"""
Phase 1: リハビリテーションデータ抽出（ワイド形式対応版）
NDB Open Data No.10「H_リハビリテーション 都道府県別算定回数／単位数.xlsx」から
都道府県別・リハビリ種別の算定回数を抽出する。

Excel構造:
  行0: 説明文（長テキスト）
  行1: NaN
  行2: カラムヘッダ（行コード, 項目名称, 診療コード, 診療科, 点数, 合計, 01, 02, ...）
  行3: 都道府県名（NaN, NaN, NaN, NaN, NaN, NaN, 北海道, 青森県, ...）
  行4+: データ（H000〜H008の各行、複数行で1コード、列0はffill要）

NDBコード（実際の意味）:
  H000: 心大血管疾患リハビリテーション料
  H001: 脳血管疾患等リハビリテーション料
  H002: 廃用症候群リハビリテーション料  <- 骨折後廃用予防に最重要
  H003: 運動器リハビリテーション料      <- 整形外科・骨折に直接関連
  H004: 呼吸器リハビリテーション料

出力: 02_Data/interim/rehabilitation_prefecture.csv
"""
import os
import sys
import pandas as pd
import numpy as np
import yaml

PROJECT_ROOT = "C:/Users/user/.ag-cursor-common/research_workspace/projects/NDB_Research_Hub"
PROJECT_DIR = os.path.join(PROJECT_ROOT, "projects", "NDB_XXX_rehabilitation_regional")
sys.path.append(os.path.join(PROJECT_ROOT, "src"))

from ndb_library.utils import clean_numeric
from ndb_library.logger import setup_logger

LOG_DIR = os.path.join(PROJECT_DIR, "03_Analysis", "analysis", "logs")
os.makedirs(LOG_DIR, exist_ok=True)
logger = setup_logger(__name__, log_file=os.path.join(LOG_DIR, "phase1_extract.log"))

with open(os.path.join(PROJECT_DIR, "config", "config.yaml"), "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

NDB_ROOT = config["data_sources"]["ndb_root"]
OUTPUT_DIR = os.path.join(PROJECT_DIR, config["output"]["interim_dir"])
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ========================================
# Step 1: Excelファイル読み込み（ヘッダなし）
# ========================================
rehab_path = os.path.join(NDB_ROOT, config["data_sources"]["rehabilitation"]["path"])
logger.info(f"リハビリExcelを読み込みます: {rehab_path}")

df_raw = pd.read_excel(rehab_path, header=None)
logger.info(f"生データサイズ: {df_raw.shape}")

# ========================================
# Step 2: Excel構造の確認と都道府県列マッピング構築
# ========================================
# 行3に都道府県名が入っている
PREF_ROW_IDX = 3
pref_row = df_raw.iloc[PREF_ROW_IDX]

# 列6以降が都道府県（47都道府県）
PREF_START_COL = 6
pref_mapping = {}  # {col_index: 都道府県名}
for col_idx in range(PREF_START_COL, df_raw.shape[1]):
    pref_name = pref_row.iloc[col_idx]
    if pd.notna(pref_name) and str(pref_name).strip():
        pref_mapping[col_idx] = str(pref_name).strip()

logger.info(f"都道府県列マッピング: {len(pref_mapping)}都道府県")
logger.info(f"最初の5都道府県: {list(pref_mapping.items())[:5]}")
logger.info(f"最後の5都道府県: {list(pref_mapping.items())[-5:]}")

assert len(pref_mapping) == 47, f"都道府県数が47でない: {len(pref_mapping)}"

# ========================================
# Step 3: データ行の抽出（行4以降）
# ========================================
DATA_START_ROW = 4
df_data = df_raw.iloc[DATA_START_ROW:].copy().reset_index(drop=True)
logger.info(f"データ行数: {len(df_data)}")

# 列0（H-code）の前方補完
logger.info(f"列0（H-code）の全値: {df_data.iloc[:, 0].tolist()}")
df_data.iloc[:, 0] = df_data.iloc[:, 0].ffill()

# ========================================
# Step 4: ターゲットコード別に都道府県合計を集計
# ========================================
# H002=廃用症候群、H003=運動器 が骨折アウトカムとの関連で最重要
TARGET_CODES = ["H000", "H001", "H002", "H003", "H004"]

results = []
for code in TARGET_CODES:
    # 完全一致のみ（H003-2等のサブコードは除外）
    mask = df_data.iloc[:, 0].astype(str) == code
    df_code = df_data[mask]
    logger.info(f"{code}: {len(df_code)}行")

    if len(df_code) == 0:
        logger.warning(f"{code} の行が見つかりませんでした")
        continue

    for col_idx, pref_name in pref_mapping.items():
        col_vals = pd.to_numeric(df_data.loc[mask, col_idx], errors="coerce")
        total = col_vals.sum()
        results.append({
            "prefecture": pref_name,
            "code": code,
            "count": total
        })

df_long = pd.DataFrame(results)
logger.info(f"集計後行数: {len(df_long)}")

# ピボット: prefecture × code
df_pivot = df_long.pivot(index="prefecture", columns="code", values="count").reset_index()
df_pivot.columns.name = None

col_rename = {
    "H000": "h000_count",
    "H001": "h001_count",
    "H002": "h002_count",
    "H003": "h003_count",
    "H004": "h004_count",
}
df_pivot = df_pivot.rename(columns=col_rename)
logger.info(f"ピボット後カラム: {df_pivot.columns.tolist()}")

# 総リハビリ算定回数
available_codes = [c for c in col_rename.values() if c in df_pivot.columns]
df_pivot["rehab_total_count"] = df_pivot[available_codes].sum(axis=1)

logger.info(f"\n記述統計（算定回数）:\n{df_pivot[available_codes + ['rehab_total_count']].describe().to_string()}")

# ========================================
# Step 5: 人口データ結合 → 算定率算出
# ========================================
pop_path = config["data_sources"]["population_stats"]["path"]
logger.info(f"人口データ読み込み: {pop_path}")
df_pop = pd.read_csv(pop_path, encoding="utf-8")
logger.info(f"人口データカラム: {df_pop.columns.tolist()}")

df_merged = pd.merge(df_pivot, df_pop[["prefecture", "total_pop", "aging_rate", "pop_density"]],
                     on="prefecture", how="left")
logger.info(f"結合後: {len(df_merged)}行, 欠損値:\n{df_merged.isna().sum()}")

# 算定率（/人口10万人）
for code_col in available_codes + ["rehab_total_count"]:
    rate_col = code_col.replace("_count", "_rate")
    df_merged[rate_col] = df_merged[code_col] / df_merged["total_pop"] * 100_000

rate_cols = [c.replace("_count", "_rate") for c in available_codes] + ["rehab_total_rate"]
logger.info(f"\nリハビリ算定率（/10万人）基本統計:\n{df_merged[rate_cols].describe().to_string()}")

# ========================================
# Step 6: 保存
# ========================================
output_path = os.path.join(OUTPUT_DIR, config["output"]["files"]["rehabilitation_data"])
df_merged.to_csv(output_path, index=False, encoding="utf-8")
logger.info(f"リハビリデータ保存完了: {output_path} ({len(df_merged)}行)")

logger.info(f"\nリハビリ総算定率（上位5）:\n{df_merged.nlargest(5, 'rehab_total_rate')[['prefecture', 'rehab_total_rate']].to_string()}")
logger.info(f"\nリハビリ総算定率（下位5）:\n{df_merged.nsmallest(5, 'rehab_total_rate')[['prefecture', 'rehab_total_rate']].to_string()}")
logger.info("Phase 1 完了")
