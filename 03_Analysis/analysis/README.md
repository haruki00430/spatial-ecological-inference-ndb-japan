# Analysis Scripts / 解析スクリプト解説

Scripts for reproducing the spatial ecological analysis in:

> Saito H, Ohira T. *How Spatial Dependence Alters Ecological Interpretation of Administrative Healthcare Data* (Spatial and Spatio-temporal Epidemiology, under review, 2026).

---

## Execution order / 実行順序

### Full pipeline (requires NDB Excel + ndb_library)

```bash
python 03_Analysis/analysis/01_extract_rehabilitation_data.py
python 03_Analysis/analysis/02_extract_fracture_outcome.py
python 03_Analysis/analysis/03_integrate_and_analyze.py
python 03_Analysis/analysis/05_spatial_regression.py
python 03_Analysis/analysis/04_visualization.py
```

### Minimal reproduction (reviewers)

```bash
cp data/release/analysis_dataset_prefecture_n47.csv 02_Data/interim/analysis_dataset.csv
python 03_Analysis/analysis/05_spatial_regression.py
python 03_Analysis/analysis/04_visualization.py
```

---

## Script descriptions / スクリプト詳細

### `01_extract_rehabilitation_data.py`

**Purpose (EN):** Extracts prefecture-level rehabilitation claim counts (H000–H004) from NDB Open Data No.10 Excel and computes per-100,000 rates.

**目的（日本語）:** NDB第10回「H_リハビリテーション」Excelから都道府県別算定回数を抽出し、人口10万人当たり算定率を計算する。

**Output:** `02_Data/interim/rehabilitation_prefecture.csv`

---

### `02_extract_fracture_outcome.py`

**Purpose (EN):** Merges hip fracture surgery rates from companion fracture dataset with population denominators.

**目的（日本語）:** 骨折手術データと人口分母を統合し、大腿骨骨折手術率を算出する。

**Output:** `02_Data/interim/fracture_outcome.csv`

---

### `03_integrate_and_analyze.py`

**Purpose (EN):** Merges rehabilitation and fracture datasets; runs OLS regression with six pre-specified sensitivity specifications.

**目的（日本語）:** リハビリと骨折データを統合し、6仕様のOLS回帰・感度分析を実行する。

**Outputs:** `02_Data/interim/analysis_dataset.csv`, `03_Analysis/results/regression_results.csv`

---

### `05_spatial_regression.py`

**Purpose (EN):** Computes Global Moran's I, Lagrange Multiplier tests, Spatial Lag Model (SLM), and Spatial Error Model (SEM) for the primary exposure–outcome pair.

**目的（日本語）:** Global Moran's I、LM検定、SLM、SEMを推定し、空間依存がOLS結果をどう変えるかを評価する。

**Inputs:** `analysis_dataset.csv`, `data/master/japan_prefectures.geojson`

**Output:** `03_Analysis/results/spatial_regression_results.csv`

**Key results:**

| Model | Rehab β | p | AIC |
|-------|---------|---|-----|
| OLS | 0.0005 | <0.001 | 447.58 |
| SEM | 0.000164 | 0.130 | 430.95 |

---

### `04_visualization.py`

**Purpose (EN):** Generates choropleth maps, scatter plots, forest plot, and correlation heatmap (300 dpi PNG).

**目的（日本語）:** 論文用の地図・散布図・Forest plot・相関ヒートマップを生成する。

**Outputs:** `03_Analysis/results/figures/fig1_*.png` … `fig7_*.png`

---

## Shared utilities / 共通ユーティリティ

- `_project_paths.py` — repository root, data paths, `ndb_library` discovery
- `config/config.yaml` — data paths and analysis settings

**Last updated:** 2026-06-27
