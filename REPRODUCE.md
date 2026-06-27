# Reproduction Guide / 再現手順書

**Project:** `spatial-ecological-inference-ndb-japan`  
**Manuscript:** *How Spatial Dependence Alters Ecological Interpretation of Administrative Healthcare Data*  
**Repository:** https://github.com/haruki00430/spatial-ecological-inference-ndb-japan  
**Zenodo DOI:** `10.5281/zenodo.XXXXXXX` — *update after GitHub Release*

This guide describes how to reproduce the **prefecture-level aggregated analysis (N = 47)** reported in the manuscript.

---

## What this repository includes / 含むもの・含まないもの

| Included | Not included (download separately) |
|----------|-----------------------------------|
| Analysis scripts (`03_Analysis/analysis/`) | NDB raw Excel (MHLW portal) |
| `data/release/analysis_dataset_prefecture_n47.csv` | Individual-level claims |
| `data/master/japan_prefectures.geojson` | slope_fracture interim CSVs (for full ETL) |
| Result CSVs and figures under `03_Analysis/results/` | Files > 100 MB |

---

## System requirements / システム要件

| Item | Requirement |
|------|-------------|
| Python | 3.10 or later (3.11+ tested) |
| OS | Windows 10/11, macOS 12+, Ubuntu 20.04+ |
| RAM | 8 GB recommended (geopandas/spatial models) |
| Disk | ~50 MB (without NDB raw files) |

---

## Step 0: Clone and environment / 環境構築

```bash
git clone https://github.com/haruki00430/spatial-ecological-inference-ndb-japan.git
cd spatial-ecological-inference-ndb-japan

python -m venv .venv
.venv\Scripts\activate          # Windows
pip install -r requirements.txt
```

**Optional (full ETL from NDB Excel):** install `ndb_library` from NDB Research Hub:

```bash
pip install -e /path/to/NDB_Research_Hub
```

---

## Route 1 — Minimal reproduction (recommended for reviewers) / 最小再現

Uses **`data/release/analysis_dataset_prefecture_n47.csv`** only. **No NDB download required.**

### 1.1 Prepare interim copy

```bash
mkdir -p 02_Data/interim
cp data/release/analysis_dataset_prefecture_n47.csv 02_Data/interim/analysis_dataset.csv
```

### 1.2 OLS regression + sensitivity (already in integrated dataset)

If starting from release CSV only, run spatial analysis directly:

```bash
python 03_Analysis/analysis/05_spatial_regression.py
python 03_Analysis/analysis/04_visualization.py
```

### 1.3 Expected headline values

| Quantity | Expected | Tolerance |
|----------|----------|-----------|
| N prefectures | 47 | exact |
| OLS β (rehab → fracture, Spec1) | 0.0005 | ±0.0001 |
| SEM β (rehab → fracture) | 0.000164 | ±0.00005 |
| Moran's I (rehab) | 0.547 | ±0.01 |
| Moran's I (fracture) | 0.563 | ±0.01 |
| SEM λ | 0.671 | ±0.05 |

Outputs: `03_Analysis/results/spatial_regression_results.csv`, `03_Analysis/results/figures/*.png`

---

## Route 2 — Full rebuild from public sources / フル再構築

Follow **[`DATA_SOURCES.md`](DATA_SOURCES.md)** to download NDB Open Data No.10 and configure paths in `config/config.yaml`.

```bash
python 03_Analysis/analysis/01_extract_rehabilitation_data.py
python 03_Analysis/analysis/02_extract_fracture_outcome.py
python 03_Analysis/analysis/03_integrate_and_analyze.py
python 03_Analysis/analysis/05_spatial_regression.py
python 03_Analysis/analysis/04_visualization.py
```

Each script logs to `03_Analysis/analysis/logs/`.

---

## Zenodo ↔ GitHub release workflow / リリース手順

1. Pre-release checklist (`04_Manuscripts/submission_package_SStE/submission_workflow_SStE.md`)
2. Confirm no secrets / raw NDB in tracked files
3. Tag `v1.0.0` on GitHub
4. Enable Zenodo–GitHub integration: https://zenodo.org/account/settings/github/
5. Update Zenodo DOI in this file, `CITATION.cff`, and `Manuscript_SStE.docx`

---

## Troubleshooting / トラブルシューティング

| Issue | Action |
|-------|--------|
| `ModuleNotFoundError: ndb_library` | Required only for Route 2; use Route 1 or `pip install -e NDB_Research_Hub` |
| `FileNotFoundError: japan.geojson` | Use bundled `data/master/japan_prefectures.geojson` |
| GeoJSON prefecture name mismatch | Script merges on `nam_ja` = `prefecture` (Japanese names) |

---

## Citation / 引用

- **Paper**: Saito H, Ohira T. *Spatial and Spatio-temporal Epidemiology* (2026, under review).
- **Software/data**: See `CITATION.cff` and Zenodo DOI.
- **Primary data**: MHLW NDB Open Data (see `DATA_SOURCES.md`).

**Last updated:** 2026-06-27
