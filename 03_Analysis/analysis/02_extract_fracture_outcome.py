"""
Phase 2: Prepare hip fracture surgery outcome rates by prefecture.
Phase 2: 骨折アウトカムデータ整備

Output / 出力: 02_Data/interim/fracture_outcome.csv
"""
import os
import sys

import numpy as np
import pandas as pd
import yaml

from _project_paths import CONFIG_PATH, DATA_INTERIM, LOG_DIR, ensure_ndb_library

ensure_ndb_library()
from ndb_library.logger import setup_logger

LOG_DIR.mkdir(parents=True, exist_ok=True)
logger = setup_logger(__name__, log_file=str(LOG_DIR / "phase2_fracture.log"))

with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

OUTPUT_DIR = DATA_INTERIM
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ========================================
# Step 1: 骨折手術データ読み込み（ワイド形式）
# ========================================
fracture_path = config["data_sources"]["fracture_surgery"]["path"]
logger.info(f"骨折手術CSVを読み込みます: {fracture_path}")
df_fracture = pd.read_csv(fracture_path, encoding="utf-8")
logger.info(f"Shape: {df_fracture.shape}")
logger.info(f"利用可能コード:\n{df_fracture[['code', 'name', 'site', 'category']].to_string()}")

# ========================================
# Step 2: 都道府県名マッピング（列名 → 都道府県名）
# ========================================
PREFECTURE_MAP = {
    "01_Hokkaido": "北海道", "02_Aomori": "青森県", "03_Iwate": "岩手県",
    "04_Miyagi": "宮城県", "05_Akita": "秋田県", "06_Yamagata": "山形県",
    "07_Fukushima": "福島県", "08_Ibaraki": "茨城県", "09_Tochigi": "栃木県",
    "10_Gunma": "群馬県", "11_Saitama": "埼玉県", "12_Chiba": "千葉県",
    "13_Tokyo": "東京都", "14_Kanagawa": "神奈川県", "15_Niigata": "新潟県",
    "16_Toyama": "富山県", "17_Ishikawa": "石川県", "18_Fukui": "福井県",
    "19_Yamanashi": "山梨県", "20_Nagano": "長野県", "21_Gifu": "岐阜県",
    "22_Shizuoka": "静岡県", "23_Aichi": "愛知県", "24_Mie": "三重県",
    "25_Shiga": "滋賀県", "26_Kyoto": "京都府", "27_Osaka": "大阪府",
    "28_Hyogo": "兵庫県", "29_Nara": "奈良県", "30_Wakayama": "和歌山県",
    "31_Tottori": "鳥取県", "32_Shimane": "島根県", "33_Okayama": "岡山県",
    "34_Hiroshima": "広島県", "35_Yamaguchi": "山口県", "36_Tokushima": "徳島県",
    "37_Kagawa": "香川県", "38_Ehime": "愛媛県", "39_Kochi": "高知県",
    "40_Fukuoka": "福岡県", "41_Saga": "佐賀県", "42_Nagasaki": "長崎県",
    "43_Kumamoto": "熊本県", "44_Oita": "大分県", "45_Miyazaki": "宮崎県",
    "46_Kagoshima": "鹿児島県", "47_Okinawa": "沖縄県"
}

pref_cols = [c for c in df_fracture.columns if c in PREFECTURE_MAP]
logger.info(f"都道府県列数: {len(pref_cols)}")

# ========================================
# Step 3: 大腿骨骨折手術の集計
# ========================================
# femur サイトのみ対象
df_femur = df_fracture[df_fracture["site"] == "femur"].copy()
logger.info(f"大腿骨骨折関連コード: {df_femur['category'].tolist()}")

# 都道府県別に合計（全大腿骨骨折手術を合算）
pref_sums_all = {}
for col in pref_cols:
    pref_name = PREFECTURE_MAP[col]
    vals = pd.to_numeric(df_femur[col], errors="coerce")
    pref_sums_all[pref_name] = vals.sum()

# K082_THA（大腿骨人工関節置換術）のみ
df_tha = df_fracture[df_fracture["category"] == "K082_THA"].copy()
pref_sums_tha = {}
for col in pref_cols:
    pref_name = PREFECTURE_MAP[col]
    vals = pd.to_numeric(df_tha[col], errors="coerce")
    pref_sums_tha[pref_name] = vals.sum()

# K081_Hemiarthroplasty（人工骨頭挿入術・大腿骨）
df_hemi_femur = df_fracture[
    (df_fracture["category"] == "K081_Hemiarthroplasty") & (df_fracture["site"] == "femur")
].copy()
pref_sums_hemi = {}
for col in pref_cols:
    pref_name = PREFECTURE_MAP[col]
    vals = pd.to_numeric(df_hemi_femur[col], errors="coerce")
    pref_sums_hemi[pref_name] = vals.sum()

# ========================================
# Step 4: 人口データ結合 → 手術率算出
# ========================================
pop_path = config["data_sources"]["population_stats"]["path"]
df_pop = pd.read_csv(pop_path, encoding="utf-8")

df_out = pd.DataFrame({
    "prefecture": list(pref_sums_all.keys()),
    "hip_fracture_all_count": list(pref_sums_all.values()),
    "hip_fracture_tha_count": [pref_sums_tha.get(p, 0) for p in pref_sums_all.keys()],
    "hip_fracture_hemi_count": [pref_sums_hemi.get(p, 0) for p in pref_sums_all.keys()],
})

df_out = pd.merge(df_out, df_pop[["prefecture", "total_pop", "elderly_pop"]], on="prefecture", how="left")
logger.info(f"結合後: {len(df_out)}行, 欠損:\n{df_out.isna().sum()}")

# 手術率（/人口10万人）
df_out["hip_fracture_rate"] = df_out["hip_fracture_all_count"] / df_out["total_pop"] * 100_000
df_out["hip_fracture_tha_rate"] = df_out["hip_fracture_tha_count"] / df_out["total_pop"] * 100_000
df_out["hip_fracture_hemi_rate"] = df_out["hip_fracture_hemi_count"] / df_out["total_pop"] * 100_000

logger.info(f"\n大腿骨骨折手術率（/10万人）基本統計:\n{df_out[['hip_fracture_rate', 'hip_fracture_tha_rate', 'hip_fracture_hemi_rate']].describe().to_string()}")
logger.info(f"\n上位5:\n{df_out.nlargest(5, 'hip_fracture_rate')[['prefecture', 'hip_fracture_rate']].to_string()}")
logger.info(f"\n下位5:\n{df_out.nsmallest(5, 'hip_fracture_rate')[['prefecture', 'hip_fracture_rate']].to_string()}")

# ========================================
# Step 5: 保存
# ========================================
output_path = os.path.join(OUTPUT_DIR, config["output"]["files"]["fracture_data"])
df_out.to_csv(output_path, index=False, encoding="utf-8")
logger.info(f"骨折アウトカムデータ保存完了: {output_path} ({len(df_out)}行)")
logger.info("Phase 2 完了")
