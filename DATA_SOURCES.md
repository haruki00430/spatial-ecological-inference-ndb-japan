# Data Sources / データソース

This repository does **not** include NDB raw Excel files.  
All primary inputs are **publicly available** administrative open data.

---

## 1. NDB Open Data No.10 / NDB オープンデータ（第10回）

| Item | Details |
|------|---------|
| Provider | MHLW / 厚生労働省 |
| Portal | https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/0000177182.html |
| Period | FY2023 (April 2023 – March 2024) |
| Redistribution | **Raw files cannot be redistributed** |

### 1.1 Exposure: Rehabilitation claims / 曝露：リハビリ算定

| Item | Value |
|------|-------|
| Category | `01_医科診療行為（算定回数）/ H_リハビリテーション` |
| File | 都道府県別算定回数／単位数.xlsx |
| Codes | H000–H004 (cardiac, stroke, disuse syndrome, musculoskeletal, pulmonary) |
| Manuscript variables | `rehab_total_rate`, `h002_rate`, `h003_rate` (per 100,000) |

### 1.2 Outcome: Hip fracture surgery / アウトカム：大腿骨骨折手術

| Item | Value |
|------|-------|
| Source | NDB Open Data No.10 surgical procedure counts |
| Procedures | K044, K045, K046, K081 (hemiarthroplasty), K082 (THA) |
| Manuscript variable | `hip_fracture_rate` (per 100,000) |

**Note:** Fracture surgery counts were initially extracted in companion project `NDB_XXX_slope_fracture`. The committed `data/release/` CSV contains the merged values used in this manuscript.

---

## 2. Population statistics / 人口統計（2020年国勢調査）

| Item | Details |
|------|---------|
| Provider | Statistics Bureau / 総務省統計局 |
| Portal | https://www.e-stat.go.jp/ |
| Variables | `total_pop`, `aging_rate`, `pop_density` |

---

## 3. Prefecture boundaries / 都道府県境界

| Item | Details |
|------|---------|
| File in repo | `data/master/japan_prefectures.geojson` |
| Use | Queen contiguity spatial weights (Moran's I, SEM, SLM) |
| Original source | Administrative boundary GeoJSON (47 prefectures) |

---

## 4. Local path configuration / ローカルパス設定

For **Route 2 (full ETL)**, edit `config/config.yaml`:

```yaml
data_sources:
  ndb_root: "/your/path/to/NDB_OpenData/No.10"
  fracture_surgery:
    path: "/your/path/to/fracture_surgery_site.csv"
  population_stats:
    path: "/your/path/to/statistics_2020.csv"
```

For **Route 1 (minimal reproduction)**, use `data/release/analysis_dataset_prefecture_n47.csv` — no config changes required.

---

## 5. Data not redistributed / 再配布不可データ

- NDB raw Excel under MHLW portal terms
- Individual-level claims
- Any cell counts subject to NDB masking rules (< 10)

**Last updated:** 2026-06-27
