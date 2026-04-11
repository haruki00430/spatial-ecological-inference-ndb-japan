> **正本リポジトリ（GitHub Private）：** https://github.com/haruki00430/NDB_XXX_rehabilitation_regional

# NDB_XXX_rehabilitation_regional

## テーマ
**回復期リハビリテーション提供量の地域格差と骨折アウトカムの生態学的関連**  
Regional disparities in rehabilitation provision and fracture outcomes: An ecological study using NDB Open Data

## 研究背景
日本では高齢化に伴い骨折リスクが増加しているが、骨折後の機能回復を左右する回復期リハビリテーション（H000-H004）の提供量には著しい地域格差が存在する。NDB Open Data No.10 の医科診療行為データ（H_リハビリテーション）を用いて、都道府県別のリハビリ算定量と骨折関連アウトカムの生態学的関連を定量化する。

## 仮説
- H1: リハビリ総算定回数が多い都道府県ほど、大腿骨骨折手術後の廃用症候群管理料算定率が低い
- H2: 廃用症候群リハビリ（H004）算定量は高齢化率との交互作用を示す

## データソース
| データ | パス | 変数 |
|--------|------|------|
| H_リハビリテーション（都道府県別） | `02_Data/raw/NDB_OpenData/No.10/01_医科診療行為（算定回数）/01_公費レセプトを含まないデータ/H_リハビリテーション/都道府県別算定回数／単位数.xlsx` | H000-H004算定回数 |
| 骨折手術データ | `projects/NDB_XXX_slope_fracture/03_Analysis/data/interim/fracture_surgery_site.csv` | 大腿骨骨折手術（K082 THA）等 |
| 廃用症候群（B_医学管理） | `01_医科診療行為（算定回数）/B_医学管理等/都道府県別算定回数.xlsx` | 廃用症候群関連コード |
| 人口・高齢化率 | `projects/NDB_XXX_slope_fracture/03_Analysis/data/interim/statistics_2020.csv` | 流用 |

## 解析フロー
```
Phase 1: リハビリデータ抽出
  H_リハビリ Excel → 都道府県別 H000-H004 算定回数
  → 02_Data/interim/rehabilitation_prefecture.csv

Phase 2: アウトカムデータ整備
  骨折手術データ（slope_fracture流用）+ 廃用症候群管理料
  → 02_Data/interim/fracture_outcome.csv

Phase 3: データ統合
  → 02_Data/interim/analysis_dataset.csv（47都道府県）

Phase 4: 統計解析
  OLS回帰（曝露: リハビリ算定率、アウトカム: 骨折手術率/廃用症候群率）
  感度分析6仕様、Moran's I
  → 03_Analysis/results/

Phase 5: 可視化 → 03_Analysis/results/figures/

Phase 6: 論文執筆 → 04_Manuscripts/Manuscript_rehabilitation_regional.qmd
```

## 主要変数
- **曝露**: リハビリ総算定回数（/人口10万人）、特に H004 廃用症候群リハビリ
- **アウトカム**: 大腿骨骨折手術率（K082-THA, /人口10万人）、廃用症候群管理算定率
- **調整変数**: 高齢化率、人口密度、医師密度

## 投稿候補
- Archives of Physical Medicine and Rehabilitation（IF ~4.0）
- Journal of Rehabilitation Medicine（IF ~3.5）
- Journal of Epidemiology（IF ~2.9）
