"""
Phase 1: リハビリテーションデータ抽出
NDB Open Data No.10「H_リハビリテーション」から都道府県別の算定回数を抽出する。
対象: H000（心大血管）, H001（脳血管）, H003（呼吸器）, H004（廃用症候群）

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

logger = setup_logger(__name__, log_file=os.path.join(PROJECT_DIR, "03_Analysis", "analysis", "logs", "phase1_extract.log"))

with open(os.path.join(PROJECT_DIR, "config", "config.yaml"), "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

NDB_ROOT = config["data_sources"]["ndb_root"]
OUTPUT_DIR = os.path.join(PROJECT_DIR, config["output"]["interim_dir"])
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ========================================
# Step 1: Excelファイル読み込み
# ========================================
rehab_path = os.path.join(NDB_ROOT, config["data_sources"]["rehabilitation"]["path"])
logger.info(f"リハビリExcelを読み込みます: {rehab_path}")

df_raw = pd.read_excel(rehab_path, header=None)
logger.info(f"生データサイズ: {df_raw.shape}")
logger.info(f"先頭5行（カラム確認用）:\n{df_raw.iloc[:5, :8].to_string()}")

# ========================================
# Step 2: データ開始行の特定
# ========================================
data_start_row = None
for i, row in df_raw.iterrows():
    row_str = " ".join([str(v) for v in row.values if pd.notna(v)])
    if "全国" in row_str or "北海道" in row_str:
        data_start_row = i
        break

if data_start_row is None:
    logger.error("データ開始行が特定できませんでした")
    raise ValueError("データ開始行が特定できませんでした")

logger.info(f"データ開始行: {data_start_row}")
header_rows = list(range(data_start_row))

df = pd.read_excel(rehab_path, header=header_rows)
logger.info(f"ヘッダー付きデータ: {df.shape}")

# カラム名の確認（上位30列）
logger.info("カラム名（上位30列）:")
for i, col in enumerate(df.columns[:30]):
    logger.info(f"  列{i}: {col}")

# ========================================
# Step 3: 都道府県行の抽出
# ========================================
PREFECTURE_LIST = [
    "北海道", "青森県", "岩手県", "宮城県", "秋田県", "山形県", "福島県",
    "茨城県", "栃木県", "群馬県", "埼玉県", "千葉県", "東京都", "神奈川県",
    "新潟県", "富山県", "石川県", "福井県", "山梨県", "長野県", "岐阜県",
    "静岡県", "愛知県", "三重県", "滋賀県", "京都府", "大阪府", "兵庫県",
    "奈良県", "和歌山県", "鳥取県", "島根県", "岡山県", "広島県", "山口県",
    "徳島県", "香川県", "愛媛県", "高知県", "福岡県", "佐賀県", "長崎県",
    "熊本県", "大分県", "宮崎県", "鹿児島県", "沖縄県"
]

pref_col = df.columns[0]
df_pref = df[df[pref_col].astype(str).isin(PREFECTURE_LIST)].copy()
logger.info(f"都道府県行数: {len(df_pref)}")

df_pref = clean_numeric(df_pref)

# ========================================
# Step 4: リハビリコード別に「合計」列を特定
# ========================================
# H000, H001, H003, H004 の「計」（男女合計）算定回数列を取得
REHAB_CODES = ["H000", "H001", "H003", "H004"]

def find_code_total_col(df, code):
    """指定コードの「計」列を探す"""
    candidates = [c for c in df.columns if code in str(c)]
    if not candidates:
        return None
    # 「計」を含む列を優先
    total_cols = [c for c in candidates if "計" in str(c)]
    return total_cols[0] if total_cols else candidates[0]

code_cols = {}
for code in REHAB_CODES:
    col = find_code_total_col(df, code)
    code_cols[code] = col
    logger.info(f"{code}: 使用列 = {col}")

# ========================================
# Step 5: 出力データセット構築
# ========================================
df_out = pd.DataFrame()
df_out["prefecture"] = df_pref[pref_col].values

for code, col in code_cols.items():
    col_name = f"{code.lower()}_count"
    if col:
        df_out[col_name] = pd.to_numeric(df_pref[col].values, errors="coerce")
    else:
        logger.warning(f"{code} の列が見つかりませんでした")
        df_out[col_name] = np.nan

# 総リハビリ算定回数
available_code_cols = [f"{c.lower()}_count" for c in REHAB_CODES if code_cols.get(c)]
if available_code_cols:
    df_out["rehab_total_count"] = df_out[available_code_cols].sum(axis=1)

# ========================================
# Step 6: 人口データ結合 → 算定率算出
# ========================================
pop_path = config["data_sources"]["population_stats"]["path"]
logger.info(f"人口データ読み込み: {pop_path}")
df_pop = pd.read_csv(pop_path, encoding="utf-8")
logger.info(f"人口データカラム: {df_pop.columns.tolist()}")

# 都道府県名の統一（既存データは英語カラム名の可能性あり）
if "prefecture" not in df_pop.columns:
    # 最初の列を都道府県名として使用
    df_pop = df_pop.rename(columns={df_pop.columns[0]: "prefecture"})

df_merged = pd.merge(df_out, df_pop[["prefecture", "total_pop", "aging_rate", "pop_density"]],
                     on="prefecture", how="left")
logger.info(f"結合後: {len(df_merged)}行")

# 算定率（/人口10万人）
for code in REHAB_CODES:
    col = f"{code.lower()}_count"
    rate_col = f"{code.lower()}_rate"
    df_merged[rate_col] = df_merged[col] / df_merged["total_pop"] * 100000

df_merged["rehab_total_rate"] = df_merged["rehab_total_count"] / df_merged["total_pop"] * 100000

logger.info(f"リハビリ総算定率（/10万人）基本統計:\n{df_merged['rehab_total_rate'].describe()}")
logger.info(f"欠損値:\n{df_merged.isna().sum()}")

# ========================================
# Step 7: 保存
# ========================================
output_path = os.path.join(OUTPUT_DIR, config["output"]["files"]["rehabilitation_data"])
df_merged.to_csv(output_path, index=False, encoding="utf-8")
logger.info(f"リハビリデータ保存: {output_path} ({len(df_merged)}行)")
logger.info("Phase 1 完了")
