# data/release — Prefecture-Level Aggregated Dataset / 都道府県別集計データ

This folder contains the **prefecture-level aggregated analysis dataset** (N = 47) used in:

> Saito H, Ohira T. "How Spatial Dependence Alters Ecological Interpretation of Administrative Healthcare Data: Lessons From Rehabilitation Provision and Hip Fracture Surgery Rates in Japan." *Spatial and Spatio-temporal Epidemiology* (under review, 2026).

## Files / ファイル一覧

| File | Description |
|------|-------------|
| `analysis_dataset_prefecture_n47.csv` | Main analysis table (47 rows × 19 columns) |

## Column dictionary / 変数辞書

| Column | Unit | Description (EN) | 説明（日本語） |
|--------|------|-------------------|--------------|
| `prefecture` | — | Prefecture name (Japanese) | 都道府県名 |
| `h000_count`–`h004_count` | claims | Raw rehabilitation claim counts by NDB category | リハビリ算定回数（H000–H004） |
| `rehab_total_count` | claims | Sum of H000–H004 claims | リハビリ総算定回数 |
| `total_pop` | persons | Total population (2020 Census) | 総人口 |
| `aging_rate` | proportion | Proportion aged ≥ 65 years | 高齢化率 |
| `pop_density` | per km² | Population density | 人口密度 |
| `h000_rate`–`h004_rate` | per 100,000 | Category-specific claim rates | 種別別算定率 |
| `rehab_total_rate` | per 100,000 | Total rehabilitation claim rate | リハビリ総算定率 |
| `hip_fracture_rate` | per 100,000 | Hip fracture surgery rate (K044–K082) | 大腿骨骨折手術率 |
| `hip_fracture_tha_rate` | per 100,000 | THA-specific rate (K082) | THA手術率 |
| `hip_fracture_hemi_rate` | per 100,000 | Hemiarthroplasty rate (K081) | 人工骨頭挿入術率 |

## Data provenance / データの出典

All values are derived from **publicly available** aggregate statistics:

- NDB Open Data No.10 (FY2023 medical claims): https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/0000177182.html
- 2020 Population Census (e-Stat): https://www.e-stat.go.jp/

**NDB raw Excel files are NOT included** and cannot be redistributed (MHLW terms).

## License / ライセンス

Released under **CC BY 4.0** (see `LICENSE-DATA` in repository root).

## Headline values (from manuscript) / 主要統計値

| Quantity | Value |
|----------|-------|
| N (prefectures) | 47 |
| Rehab total rate range | 27,183–183,490 per 100,000 (6.8-fold) |
| Hip fracture rate range | 167.6–329.6 per 100,000 |
| OLS β (rehab → fracture, Spec1) | 0.0005 (p < 0.001) |
| SEM β (rehab → fracture) | 0.000164 (p = 0.130) |
| Moran's I (rehab / fracture) | 0.547 / 0.563 (both p = 0.001) |
