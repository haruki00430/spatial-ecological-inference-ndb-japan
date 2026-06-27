"""
Phase 3–4: Integrate datasets and run OLS regression with sensitivity analyses.
Phase 3–4: データ統合・OLS回帰・感度分析

Outputs / 出力: analysis_dataset.csv, regression_results.csv
"""
import os
import sys

import numpy as np
import pandas as pd
import statsmodels.api as sm
import yaml
from statsmodels.stats.outliers_influence import variance_inflation_factor

from _project_paths import (
    CONFIG_PATH,
    DATA_INTERIM,
    DATA_RELEASE,
    GEOJSON_PATH,
    LOG_DIR,
    RESULTS_DIR,
    ensure_ndb_library,
)

ensure_ndb_library()
from ndb_library.logger import setup_logger

LOG_DIR.mkdir(parents=True, exist_ok=True)
logger = setup_logger(__name__, log_file=str(LOG_DIR / "phase34_analysis.log"))

with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

INTERIM_DIR = DATA_INTERIM
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

df_rehab = pd.read_csv(INTERIM_DIR / config["output"]["files"]["rehabilitation_data"])
df_frac = pd.read_csv(INTERIM_DIR / config["output"]["files"]["fracture_data"])
df = pd.merge(df_rehab, df_frac[["prefecture","hip_fracture_rate","hip_fracture_tha_rate","hip_fracture_hemi_rate"]], on="prefecture", how="inner")
logger.info(f"統合: {len(df)}行")

key = ["rehab_total_rate","h002_rate","h003_rate","hip_fracture_rate","hip_fracture_tha_rate","aging_rate","pop_density"]
logger.info("Descriptive stats:\n" + df[key].describe().to_string())
logger.info("Correlation matrix:\n" + df[key].corr().round(3).to_string())
df.to_csv(INTERIM_DIR / config["output"]["files"]["analysis_dataset"], index=False, encoding="utf-8")

EXPOSURES = ["rehab_total_rate","h002_rate","h003_rate"]
OUTCOMES  = ["hip_fracture_rate","hip_fracture_tha_rate"]
METRO     = ["東京都","大阪府","愛知県"]

def run_ols(df_, exp, out, cov, robust=None, log_t=False, name="", outlier=False, excl=None):
    d = df_.copy()
    if outlier:
        for v in [exp, out]:
            q1,q3 = d[v].quantile([.25,.75]); iqr=q3-q1
            d = d[(d[v]>=q1-3*iqr)&(d[v]<=q3+3*iqr)]
    if excl: d = d[~d["prefecture"].isin(excl)]
    if log_t: d[exp]=np.log1p(d[exp]); d[out]=np.log1p(d[out])
    X = d[[exp]+cov].dropna(); y = d.loc[X.index, out]
    Xc = sm.add_constant(X)
    r = sm.OLS(y,Xc).fit(cov_type=robust) if robust else sm.OLS(y,Xc).fit()
    ci = r.conf_int().loc[exp]
    return dict(spec=name,exposure=exp,outcome=out,n=len(y),
                beta=round(float(r.params[exp]),4),se=round(float(r.bse[exp]),4),
                t=round(float(r.tvalues[exp]),3),p=round(float(r.pvalues[exp]),4),
                ci_lo=round(float(ci[0]),4),ci_hi=round(float(ci[1]),4),
                r2=round(float(r.rsquared),3),r2_adj=round(float(r.rsquared_adj),3))

rows=[]
for exp in EXPOSURES:
    for out in OUTCOMES:
        specs=[
          dict(name="Spec1_Baseline",       cov=["aging_rate","pop_density"]),
          dict(name="Spec2_HC3",             cov=["aging_rate","pop_density"],robust="HC3"),
          dict(name="Spec3_OutlierExcluded", cov=["aging_rate","pop_density"],outlier=True),
          dict(name="Spec4_MetroExcluded",   cov=["aging_rate","pop_density"],excl=METRO),
          dict(name="Spec5_LogTransformed",  cov=["aging_rate","pop_density"],log_t=True),
          dict(name="Spec6_AgingOnly",       cov=["aging_rate"]),
        ]
        for s in specs:
            res=run_ols(df,exp=exp,out=out,**s)
            rows.append(res)
            sig="**" if res["p"]<0.01 else ("*" if res["p"]<0.05 else "ns")
            logger.info(f"{res['spec']} | {exp}->{out}: beta={res['beta']:.3f} p={res['p']:.4f} {sig} R2={res['r2']:.3f}")

df_res = pd.DataFrame(rows)
df_res.to_csv(RESULTS_DIR / config["output"]["files"]["regression_results"], index=False, encoding="utf-8")

logger.info("\n=== Sensitivity Analysis Summary ===")
for exp in EXPOSURES:
    for out in OUTCOMES:
        sub=df_res[(df_res.exposure==exp)&(df_res.outcome==out)]
        n_sig=(sub.p<0.05).sum()
        b1=sub[sub.spec=="Spec1_Baseline"].iloc[0]
        logger.info(f"{exp}->{out}: {n_sig}/6 significant, Spec1 beta={b1['beta']:.3f} p={b1['p']:.4f}")

logger.info("\n=== VIF ===")
for exp in EXPOSURES:
    Xv=df[["aging_rate","pop_density",exp]].dropna()
    Xc=sm.add_constant(Xv)
    vs=[variance_inflation_factor(Xc.values,i+1) for i in range(Xc.shape[1]-1)]
    logger.info(f"{exp}: aging={vs[0]:.2f} pop_density={vs[1]:.2f} exposure={vs[2]:.2f}")

logger.info("\n=== Moran's I (via japan.geojson) ===")
try:
    from libpysal.weights import Queen
    from esda.moran import Moran
    import geopandas as gpd
    gdf = gpd.read_file(GEOJSON_PATH)
    gdf = gdf.merge(df, left_on="nam_ja", right_on="prefecture", how="left")
    gdf_clean = gdf.dropna(subset=["rehab_total_rate"]).copy()
    w = Queen.from_dataframe(gdf_clean)
    w.transform = "r"
    for v in ["hip_fracture_rate", "rehab_total_rate", "h002_rate"]:
        mi = Moran(gdf_clean[v], w, permutations=999)
        logger.info(f"{v}: I={mi.I:.4f} p={mi.p_sim:.4f}")
except Exception as e:
    logger.warning(f"Moran's I failed: {e}")
logger.info("Phase 3&4 complete")
