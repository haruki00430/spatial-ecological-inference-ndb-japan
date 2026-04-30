"""
Phase 3 Supplement: Spatial Regression Analysis
NDB_XXX_rehabilitation_regional

LM test-guided spatial model selection:
  1. OLS with spatial diagnostics (LM-lag, LM-error, RLM-lag, RLM-error)
  2. Spatial Lag Model (SLM) — ML estimation
  3. Spatial Error Model (SEM) — ML estimation

Primary exposure : rehab_total_rate
Primary outcome  : hip_fracture_rate
Covariates       : aging_rate, pop_density
Spatial weights  : Queen contiguity, row-standardized

Output: 03_Analysis/results/spatial_regression_results.csv
"""

import os
import sys
import pandas as pd
import numpy as np
import geopandas as gpd

PROJECT_ROOT = "C:/Users/user/.ag-cursor-common/research_workspace/projects/NDB_Research_Hub"
PROJECT_DIR  = os.path.join(PROJECT_ROOT, "projects", "NDB_XXX_rehabilitation_regional")
sys.path.append(os.path.join(PROJECT_ROOT, "src"))

from ndb_library.logger import setup_logger

LOG_DIR = os.path.join(PROJECT_DIR, "03_Analysis", "analysis", "logs")
os.makedirs(LOG_DIR, exist_ok=True)
logger = setup_logger(__name__, log_file=os.path.join(LOG_DIR, "phase_spatial_regression.log"))

RESULTS_DIR = os.path.join(PROJECT_DIR, "03_Analysis", "results")
os.makedirs(RESULTS_DIR, exist_ok=True)

# ======================================================
# Data loading
# ======================================================
df = pd.read_csv(
    os.path.join(PROJECT_DIR, "02_Data", "interim", "analysis_dataset.csv"),
    encoding="utf-8"
)
gdf = gpd.read_file(os.path.join(PROJECT_ROOT, "02_Data", "raw", "GIS", "japan.geojson"))
gdf = gdf.merge(df, left_on="nam_ja", right_on="prefecture", how="left")
gdf = gdf.dropna(subset=["rehab_total_rate", "hip_fracture_rate"]).copy().reset_index(drop=True)
logger.info(f"Spatial data: {len(gdf)} prefectures")

from libpysal.weights import Queen
w = Queen.from_dataframe(gdf, use_index=False)
w.transform = "r"
logger.info(f"Spatial weight matrix: {w.n} units, islands={list(w.islands)}")

# ======================================================
# Variable arrays
# ======================================================
EXPOSURE  = "rehab_total_rate"
OUTCOME   = "hip_fracture_rate"
COVARIATES = ["aging_rate", "pop_density"]

y = gdf[[OUTCOME]].values
X = gdf[[EXPOSURE] + COVARIATES].values
xnames = [EXPOSURE] + COVARIATES

# ======================================================
# OLS with spatial diagnostics
# ======================================================
from spreg import OLS, ML_Lag, ML_Error

ols = OLS(y, X, w=w, spat_diag=True,
          name_y=OUTCOME, name_x=xnames, name_ds="japan_prefecture")

logger.info("=== OLS with spatial diagnostics ===")
logger.info(f"  AIC={ols.aic:.3f}  R2={ols.r2:.4f}")
logger.info(f"  coef {EXPOSURE}={ols.betas[1][0]:.6f}  t={ols.t_stat[1][0]:.3f}  p={ols.t_stat[1][1]:.4f}")
logger.info(f"  LM_lag:    stat={ols.lm_lag[0]:.4f}  p={ols.lm_lag[1]:.4f}")
logger.info(f"  LM_error:  stat={ols.lm_error[0]:.4f}  p={ols.lm_error[1]:.4f}")
logger.info(f"  RLM_lag:   stat={ols.rlm_lag[0]:.4f}  p={ols.rlm_lag[1]:.4f}")
logger.info(f"  RLM_error: stat={ols.rlm_error[0]:.4f}  p={ols.rlm_error[1]:.4f}")

lm_decision = (
    "SEM" if (ols.lm_error[1] < 0.05 and ols.rlm_error[1] < ols.rlm_lag[1])
    else "SLM" if (ols.lm_lag[1] < 0.05 and ols.rlm_lag[1] < ols.rlm_error[1])
    else "OLS"
)
logger.info(f"  LM cascade decision: {lm_decision}")

# ======================================================
# Spatial Lag Model
# ======================================================
slm = ML_Lag(y, X, w=w, name_y=OUTCOME, name_x=xnames)

logger.info("=== Spatial Lag Model (SLM) ===")
logger.info(f"  AIC={slm.aic:.3f}  Pseudo-R2={slm.pr2:.4f}")
logger.info(f"  rho={slm.betas[-1][0]:.4f}  z={slm.z_stat[-1][0]:.3f}  p={slm.z_stat[-1][1]:.4f}")
logger.info(f"  coef {EXPOSURE}={slm.betas[1][0]:.6f}  z={slm.z_stat[1][0]:.3f}  p={slm.z_stat[1][1]:.4f}")

# ======================================================
# Spatial Error Model
# ======================================================
sem = ML_Error(y, X, w=w, name_y=OUTCOME, name_x=xnames)

logger.info("=== Spatial Error Model (SEM) ===")
logger.info(f"  AIC={sem.aic:.3f}  Pseudo-R2={sem.pr2:.4f}")
logger.info(f"  lambda={sem.betas[-1][0]:.4f}  z={sem.z_stat[-1][0]:.3f}  p={sem.z_stat[-1][1]:.4f}")
logger.info(f"  coef {EXPOSURE}={sem.betas[1][0]:.6f}  z={sem.z_stat[1][0]:.3f}  p={sem.z_stat[1][1]:.4f}")

logger.info(f"AIC: OLS={ols.aic:.2f}  SLM={slm.aic:.2f}  SEM={sem.aic:.2f} (best: {lm_decision})")

# ======================================================
# Save structured results
# ======================================================
rows = [
    dict(model="OLS",
         exposure_coef=round(float(ols.betas[1][0]), 6),
         exposure_stat=round(float(ols.t_stat[1][0]), 3),
         exposure_p=round(float(ols.t_stat[1][1]), 4),
         spatial_param=None,
         spatial_stat=None,
         spatial_p=None,
         aic=round(ols.aic, 3),
         r2_or_pr2=round(ols.r2, 4),
         lm_lag_p=round(ols.lm_lag[1], 4),
         lm_error_p=round(ols.lm_error[1], 4),
         rlm_lag_p=round(ols.rlm_lag[1], 4),
         rlm_error_p=round(ols.rlm_error[1], 4)),
    dict(model="SLM",
         exposure_coef=round(float(slm.betas[1][0]), 6),
         exposure_stat=round(float(slm.z_stat[1][0]), 3),
         exposure_p=round(float(slm.z_stat[1][1]), 4),
         spatial_param=round(float(slm.betas[-1][0]), 4),
         spatial_stat=round(float(slm.z_stat[-1][0]), 3),
         spatial_p=round(float(slm.z_stat[-1][1]), 4),
         aic=round(slm.aic, 3),
         r2_or_pr2=round(slm.pr2, 4),
         lm_lag_p=None, lm_error_p=None, rlm_lag_p=None, rlm_error_p=None),
    dict(model="SEM",
         exposure_coef=round(float(sem.betas[1][0]), 6),
         exposure_stat=round(float(sem.z_stat[1][0]), 3),
         exposure_p=round(float(sem.z_stat[1][1]), 4),
         spatial_param=round(float(sem.betas[-1][0]), 4),
         spatial_stat=round(float(sem.z_stat[-1][0]), 3),
         spatial_p=round(float(sem.z_stat[-1][1]), 4),
         aic=round(sem.aic, 3),
         r2_or_pr2=round(sem.pr2, 4),
         lm_lag_p=None, lm_error_p=None, rlm_lag_p=None, rlm_error_p=None),
]

out_path = os.path.join(RESULTS_DIR, "spatial_regression_results.csv")
pd.DataFrame(rows).to_csv(out_path, index=False, encoding="utf-8")
logger.info(f"Saved: {out_path}")
logger.info("Phase spatial regression complete")
print("Spatial regression complete")
print(f"LM cascade → {lm_decision} selected")
print(f"SEM coef={sem.betas[1][0]:.6f} p={sem.z_stat[1][1]:.4f}")
