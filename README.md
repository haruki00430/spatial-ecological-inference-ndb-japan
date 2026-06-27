> **正本リポジトリ (GitHub):** https://github.com/haruki00430/spatial-ecological-inference-ndb-japan  
> **再現・公開:** [`REPRODUCE.md`](REPRODUCE.md) · [`DATA_SOURCES.md`](DATA_SOURCES.md) · [`03_Analysis/analysis/README.md`](03_Analysis/analysis/README.md) · [`CITATION.cff`](CITATION.cff)

# How Spatial Dependence Alters Ecological Interpretation

## Rehabilitation Provision and Hip Fracture Surgery Rates in Japan — Prefecture-Level Spatial Ecological Analysis

**論文タイトル（日本語）**: 空間依存が行政医療データの生態学的解釈をいかに変えるか——リハビリ提供量と大腿骨骨折手術率に関する全国47都道府県の事例

**Manuscript status**: Under review at *Spatial and Spatio-temporal Epidemiology* (2026-06-27 submission)  
**Repository:** https://github.com/haruki00430/spatial-ecological-inference-ndb-japan  
**Zenodo DOI:** https://doi.org/10.5281/zenodo.20951654

---

## Abstract / 研究概要

We examined whether the apparent ecological association between prefecture-level rehabilitation claim rates and hip fracture surgery rates in Japan changes after accounting for spatial dependence. Using NDB Open Data No.10 (FY2023, N = 47), OLS models showed a positive association robust across six sensitivity specifications, but a Lagrange-Multiplier-preferred Spatial Error Model attenuated the coefficient to non-significance (β = 0.000164, p = 0.130; ΔAIC = −16.6). This empirical example supports routine spatial diagnostics in ecological analyses of administrative healthcare data.

日本47都道府県のNDB Open Data（第10回・2023年度）を用い、リハビリ算定率と大腿骨骨折手術率の生態学的関連が空間依存の調整後にどう変化するかを検討した。OLSでは6つの感度分析すべてで正の関連が得られたが、Spatial Error Modelでは係数は非有意に attenuate された（β = 0.000164, p = 0.130）。行政オープンデータを用いる生態学的解析において空間診断を routine 化する必要性を示す。

---

## Repository structure / リポジトリ構造

```
spatial-ecological-inference-ndb-japan/
├── 03_Analysis/
│   ├── analysis/              # Analysis scripts (01–05) / 解析スクリプト
│   │   ├── README.md          # Script guide / スクリプト解説
│   │   ├── 01_extract_rehabilitation_data.py
│   │   ├── 02_extract_fracture_outcome.py
│   │   ├── 03_integrate_and_analyze.py
│   │   ├── 04_visualization.py
│   │   └── 05_spatial_regression.py
│   └── results/
│       └── figures/           # Output figures (PNG, 300 dpi)
├── config/config.yaml         # Project settings / プロジェクト設定
├── data/
│   ├── release/               # Public aggregated data (N = 47)
│   │   ├── analysis_dataset_prefecture_n47.csv
│   │   └── README.md
│   └── master/
│       └── japan_prefectures.geojson
├── 04_Manuscripts/
│   └── submission_package_SStE/  # SStE submission files
├── REPRODUCE.md
├── DATA_SOURCES.md
├── CITATION.cff
├── LICENSE                      # MIT (code)
├── LICENSE-DATA                 # CC BY 4.0 (data/release/)
└── requirements.txt
```

---

## Quick start / クイックスタート

```bash
git clone https://github.com/haruki00430/spatial-ecological-inference-ndb-japan.git
cd spatial-ecological-inference-ndb-japan

python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # macOS/Linux

pip install -r requirements.txt
# ndb_library (optional for full ETL): pip install -e /path/to/NDB_Research_Hub
```

### Minimal reproduction (no NDB download) / 最小再現

```bash
# Copy release CSV to interim (or scripts read data/release directly)
python 03_Analysis/analysis/03_integrate_and_analyze.py
python 03_Analysis/analysis/05_spatial_regression.py
python 03_Analysis/analysis/04_visualization.py
```

See **[REPRODUCE.md](REPRODUCE.md)** for full details.

---

## Data sources / データソース

| Source | Description | URL |
|--------|-------------|-----|
| NDB Open Data No.10 | Rehabilitation claims (H000–H004), fracture surgery | https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/0000177182.html |
| 2020 Population Census | Aging rate, population density | https://www.e-stat.go.jp/ |
| Prefecture boundaries | GeoJSON for spatial weights | `data/master/japan_prefectures.geojson` |

**NDB raw Excel files are NOT included.** See [DATA_SOURCES.md](DATA_SOURCES.md).

---

## Key results / 主要結果

| Analysis | Result |
|----------|--------|
| OLS β (rehab → fracture, Spec1) | 0.0005 (p < 0.001; 6/6 specs significant) |
| SEM β (rehab → fracture) | 0.000164 (p = 0.130) |
| Moran's I (rehab / fracture) | 0.547 / 0.563 (p = 0.001) |
| SEM vs OLS | ΔAIC = −16.6; λ = 0.671 (p < 0.001) |

---

## Authors / 著者

| Name | Affiliation | ORCID |
|------|-------------|-------|
| **Haruki Saito** (Corresponding) | Department of Epidemiology, Fukushima Medical University School of Medicine | [0009-0009-7890-6068](https://orcid.org/0009-0009-7890-6068) |
| Tetsuya Ohira | Department of Epidemiology, Fukushima Medical University School of Medicine | [0000-0003-4532-7165](https://orcid.org/0000-0003-4532-7165) |

---

## Citation / 引用

```
Saito H, Ohira T. How Spatial Dependence Alters Ecological Interpretation of
Administrative Healthcare Data: Lessons From Rehabilitation Provision and Hip
Fracture Surgery Rates in Japan. Spatial and Spatio-temporal Epidemiology
(under review, 2026).
GitHub: https://github.com/haruki00430/spatial-ecological-inference-ndb-japan
Zenodo: https://doi.org/10.5281/zenodo.20951654
```

See [`CITATION.cff`](CITATION.cff) for machine-readable metadata.

---

## License / ライセンス

- **Code**: [MIT License](LICENSE)
- **Aggregated data** (`data/release/`): [CC BY 4.0](LICENSE-DATA)
- **NDB raw data**: Not included; MHLW portal terms apply

**Last updated**: 2026-06-27
