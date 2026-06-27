"""
Phase 5: 可視化（Visualization）
NDB_XXX_rehabilitation_regional

出力図一覧:
  Fig1: Choropleth map — リハビリ総算定率（都道府県別）
  Fig2: Choropleth map — 大腿骨骨折手術率（都道府県別）
  Fig3: Scatter plot — rehab_total_rate vs hip_fracture_rate
  Fig4: Scatter plot — h002_rate vs hip_fracture_rate
  Fig5: Scatter plot — h003_rate vs hip_fracture_rate
  Fig6: Forest plot — 感度分析6仕様（rehab_total_rate → hip_fracture_rate）
  Fig7: Correlation heatmap

出力先: 03_Analysis/results/figures/
"""

import os
import sys

import geopandas as gpd
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import pandas as pd
import seaborn as sns
from scipy import stats

matplotlib.use("Agg")

from _project_paths import (
    DATA_INTERIM,
    DATA_RELEASE,
    FIGURES_DIR,
    GEOJSON_PATH,
    LOG_DIR,
    RESULTS_DIR,
    ensure_ndb_library,
)

ensure_ndb_library()
from ndb_library.logger import setup_logger
from ndb_library.viz import set_japanese_font

set_japanese_font()

LOG_DIR.mkdir(parents=True, exist_ok=True)
logger = setup_logger(__name__, log_file=str(LOG_DIR / "phase5_visualization.log"))

FIGURES_DIR.mkdir(parents=True, exist_ok=True)

PREF_EN = {
    "北海道": "Hokkaido", "青森県": "Aomori", "岩手県": "Iwate", "宮城県": "Miyagi",
    "秋田県": "Akita", "山形県": "Yamagata", "福島県": "Fukushima", "茨城県": "Ibaraki",
    "栃木県": "Tochigi", "群馬県": "Gunma", "埼玉県": "Saitama", "千葉県": "Chiba",
    "東京都": "Tokyo", "神奈川県": "Kanagawa", "新潟県": "Niigata", "富山県": "Toyama",
    "石川県": "Ishikawa", "福井県": "Fukui", "山梨県": "Yamanashi", "長野県": "Nagano",
    "岐阜県": "Gifu", "静岡県": "Shizuoka", "愛知県": "Aichi", "三重県": "Mie",
    "滋賀県": "Shiga", "京都府": "Kyoto", "大阪府": "Osaka", "兵庫県": "Hyogo",
    "奈良県": "Nara", "和歌山県": "Wakayama", "鳥取県": "Tottori", "島根県": "Shimane",
    "岡山県": "Okayama", "広島県": "Hiroshima", "山口県": "Yamaguchi", "徳島県": "Tokushima",
    "香川県": "Kagawa", "愛媛県": "Ehime", "高知県": "Kochi", "福岡県": "Fukuoka",
    "佐賀県": "Saga", "長崎県": "Nagasaki", "熊本県": "Kumamoto", "大分県": "Oita",
    "宮崎県": "Miyazaki", "鹿児島県": "Kagoshima", "沖縄県": "Okinawa",
}

# ======================================================
# データ読み込み
# ======================================================
dataset_path = DATA_INTERIM / "analysis_dataset.csv"
if not dataset_path.exists():
    dataset_path = DATA_RELEASE / "analysis_dataset_prefecture_n47.csv"
df = pd.read_csv(dataset_path, encoding="utf-8")

regression_path = RESULTS_DIR / "regression_results.csv"
if not regression_path.exists():
    raise FileNotFoundError(
        "regression_results.csv not found. Run 03_integrate_and_analyze.py first."
    )
df_reg = pd.read_csv(regression_path, encoding="utf-8")

gdf = gpd.read_file(GEOJSON_PATH)
gdf = gdf.merge(df, left_on="nam_ja", right_on="prefecture", how="left")

logger.info(f"分析データ: {df.shape}, 回帰結果: {df_reg.shape}, GeoJSON: {gdf.shape}")


# ======================================================
# Fig1: Choropleth — リハビリ総算定率
# ======================================================
def fig1_choropleth_rehab():
    fig, ax = plt.subplots(1, 1, figsize=(10, 8))
    gdf.plot(
        column="rehab_total_rate",
        ax=ax,
        legend=True,
        cmap="YlOrRd",
        legend_kwds={
            "label": "Total Rehabilitation Claim Rate (per 100,000)",
            "orientation": "horizontal",
            "shrink": 0.7,
            "pad": 0.02,
        },
        edgecolor="white",
        linewidth=0.3,
        missing_kwds={"color": "lightgrey", "label": "No data"},
    )
    ax.set_title("Prefectural Total Rehabilitation Claim Rate\n(NDB Open Data No.10, FY2023)",
                 fontsize=13, pad=12)
    ax.axis("off")
    out = os.path.join(FIGURES_DIR, "fig1_choropleth_rehab_rate.png")
    fig.savefig(out, dpi=300, bbox_inches="tight")
    plt.close(fig)
    logger.info(f"Fig1保存: {out}")


# ======================================================
# Fig2: Choropleth — 大腿骨骨折手術率
# ======================================================
def fig2_choropleth_fracture():
    fig, ax = plt.subplots(1, 1, figsize=(10, 8))
    gdf.plot(
        column="hip_fracture_rate",
        ax=ax,
        legend=True,
        cmap="Blues",
        legend_kwds={
            "label": "Hip Fracture Surgery Rate (per 100,000)",
            "orientation": "horizontal",
            "shrink": 0.7,
            "pad": 0.02,
        },
        edgecolor="white",
        linewidth=0.3,
        missing_kwds={"color": "lightgrey", "label": "No data"},
    )
    ax.set_title("Prefectural Hip Fracture Surgery Rate\n(NDB Open Data No.10, FY2023)",
                 fontsize=13, pad=12)
    ax.axis("off")
    out = os.path.join(FIGURES_DIR, "fig2_choropleth_fracture_rate.png")
    fig.savefig(out, dpi=300, bbox_inches="tight")
    plt.close(fig)
    logger.info(f"Fig2保存: {out}")


# ======================================================
# Fig3: Scatter — rehab_total_rate vs hip_fracture_rate
# ======================================================
def fig3_scatter_main():
    x = df["rehab_total_rate"]
    y = df["hip_fracture_rate"]
    slope, intercept, r, p, se = stats.linregress(x, y)

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.scatter(x, y, color="#2166ac", alpha=0.7, edgecolors="white", s=60, zorder=3)

    x_line = np.linspace(x.min(), x.max(), 200)
    ax.plot(x_line, slope * x_line + intercept, color="#d73027", lw=2, label=f"OLS regression line (r={r:.3f}, p={p:.4f})")

    # Prefecture labels for outliers (top/bottom 5 by residual)
    residuals = y - (slope * x + intercept)
    label_mask = (residuals.abs() > residuals.abs().quantile(0.80))
    for i, row in df[label_mask].iterrows():
        ax.annotate(
            PREF_EN.get(row["prefecture"], row["prefecture"]),
            (row["rehab_total_rate"], row["hip_fracture_rate"]),
            fontsize=7, ha="left", va="bottom",
            xytext=(3, 3), textcoords="offset points",
        )

    ax.set_xlabel("Total Rehabilitation Claim Rate (per 100,000)", fontsize=11)
    ax.set_ylabel("Hip Fracture Surgery Rate (per 100,000)", fontsize=11)
    ax.set_title("Association between Total Rehabilitation Claim Rate\nand Hip Fracture Surgery Rate (Prefectures, N=47)", fontsize=12)
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)

    out = os.path.join(FIGURES_DIR, "fig3_scatter_rehab_fracture.png")
    fig.savefig(out, dpi=300, bbox_inches="tight")
    plt.close(fig)
    logger.info(f"Fig3保存: {out}")


# ======================================================
# Fig4: Scatter — h002_rate vs hip_fracture_rate
# ======================================================
def fig4_scatter_h002():
    x = df["h002_rate"]
    y = df["hip_fracture_rate"]
    slope, intercept, r, p, se = stats.linregress(x, y)

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.scatter(x, y, color="#4dac26", alpha=0.7, edgecolors="white", s=60, zorder=3)
    x_line = np.linspace(x.min(), x.max(), 200)
    ax.plot(x_line, slope * x_line + intercept, color="#d73027", lw=2,
            label=f"OLS regression line (r={r:.3f}, p={p:.4f})")

    ax.set_xlabel("Disuse Syndrome Rehabilitation Claim Rate (H002, per 100,000)", fontsize=11)
    ax.set_ylabel("Hip Fracture Surgery Rate (per 100,000)", fontsize=11)
    ax.set_title("Association between Disuse Syndrome Rehabilitation Rate (H002)\nand Hip Fracture Surgery Rate (Prefectures, N=47)", fontsize=12)
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)

    out = os.path.join(FIGURES_DIR, "fig4_scatter_h002_fracture.png")
    fig.savefig(out, dpi=300, bbox_inches="tight")
    plt.close(fig)
    logger.info(f"Fig4保存: {out}")


# ======================================================
# Fig5: Scatter — h003_rate vs hip_fracture_rate
# ======================================================
def fig5_scatter_h003():
    x = df["h003_rate"]
    y = df["hip_fracture_rate"]
    slope, intercept, r, p, se = stats.linregress(x, y)

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.scatter(x, y, color="#762a83", alpha=0.7, edgecolors="white", s=60, zorder=3)
    x_line = np.linspace(x.min(), x.max(), 200)
    ax.plot(x_line, slope * x_line + intercept, color="#d73027", lw=2,
            label=f"OLS regression line (r={r:.3f}, p={p:.4f})")

    ax.set_xlabel("Musculoskeletal Rehabilitation Claim Rate (H003, per 100,000)", fontsize=11)
    ax.set_ylabel("Hip Fracture Surgery Rate (per 100,000)", fontsize=11)
    ax.set_title("Association between Musculoskeletal Rehabilitation Rate (H003)\nand Hip Fracture Surgery Rate (Prefectures, N=47)", fontsize=12)
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)

    out = os.path.join(FIGURES_DIR, "fig5_scatter_h003_fracture.png")
    fig.savefig(out, dpi=300, bbox_inches="tight")
    plt.close(fig)
    logger.info(f"Fig5保存: {out}")


# ======================================================
# Fig6: Forest plot — 感度分析6仕様
# ======================================================
def fig6_forest_plot():
    """
    曝露: rehab_total_rate → アウトカム: hip_fracture_rate の6仕様感度分析
    """
    sub = df_reg[
        (df_reg["exposure"] == "rehab_total_rate") &
        (df_reg["outcome"] == "hip_fracture_rate")
    ].copy()

    spec_labels = {
        "Spec1_Baseline": "Spec 1: Baseline OLS\n(adjusted for aging_rate + pop_density)",
        "Spec2_HC3": "Spec 2: HC3 Robust SE",
        "Spec3_OutlierExcluded": "Spec 3: Outlier Exclusion (±3 IQR)",
        "Spec4_MetroExcluded": "Spec 4: Metropolitan Exclusion\n(Tokyo, Osaka, Aichi, Kanagawa, Saitama, Chiba)",
        "Spec5_LogTransformed": "Spec 5: Log-Transformed (log-log)",
        "Spec6_AgingOnly": "Spec 6: Aging Rate Only",
    }

    sub["label"] = sub["spec"].map(spec_labels)
    sub = sub.reset_index(drop=True)

    fig, ax = plt.subplots(figsize=(10, 6))
    y_pos = np.arange(len(sub))

    # Plot each spec separately so per-row colors are supported
    x_right = sub["ci_hi"].max() * 1.05
    for i, (_, row) in enumerate(sub.iterrows()):
        c = "#d73027" if row["p"] < 0.05 else "#74c476"
        ax.errorbar(
            row["beta"], i,
            xerr=[[row["beta"] - row["ci_lo"]], [row["ci_hi"] - row["beta"]]],
            fmt="o", color=c, ecolor=c,
            capsize=4, markersize=7, linewidth=1.5, elinewidth=1.5,
        )
        p_str = f"p={row['p']:.4f}" if row["p"] >= 0.001 else "p<0.001"
        ax.text(
            x_right, i,
            f"β={row['beta']:.5f} ({p_str})",
            va="center", fontsize=8, color=c,
        )

    ax.axvline(0, color="black", lw=0.8, ls="--", alpha=0.6)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(sub["label"], fontsize=9)
    ax.set_xlabel("Regression Coefficient β (95% CI)", fontsize=11)
    ax.set_title(
        "Sensitivity Analysis: Total Rehabilitation Claim Rate → Hip Fracture Surgery Rate\n(6 specifications, N=47 prefectures)",
        fontsize=12
    )

    sig_patch = mpatches.Patch(color="#d73027", label="p < 0.05")
    ns_patch = mpatches.Patch(color="#74c476", label="p ≥ 0.05")
    ax.legend(handles=[sig_patch, ns_patch], loc="lower right", fontsize=9)

    ax.grid(True, axis="x", alpha=0.3)
    fig.tight_layout()

    out = os.path.join(FIGURES_DIR, "fig6_forest_sensitivity.png")
    fig.savefig(out, dpi=300, bbox_inches="tight")
    plt.close(fig)
    logger.info(f"Fig6保存: {out}")


# ======================================================
# Fig7: Correlation heatmap
# ======================================================
def fig7_correlation_heatmap():
    cols = [
        "rehab_total_rate", "h002_rate", "h003_rate",
        "hip_fracture_rate", "hip_fracture_tha_rate",
        "aging_rate", "pop_density",
    ]
    col_labels = [
        "Rehab total rate", "Disuse rehab (H002)",
        "Musculoskeletal rehab (H003)",
        "Hip fracture rate", "THA rate",
        "Aging rate", "Population density",
    ]
    corr = df[cols].corr()

    fig, ax = plt.subplots(figsize=(8, 7))
    mask = np.triu(np.ones_like(corr, dtype=bool), k=1)  # upper triangle off

    sns.heatmap(
        corr,
        ax=ax,
        annot=True,
        fmt=".2f",
        cmap="RdBu_r",
        center=0,
        vmin=-1, vmax=1,
        xticklabels=col_labels,
        yticklabels=col_labels,
        linewidths=0.5,
        annot_kws={"size": 8},
    )
    ax.set_title("Correlation Matrix of Key Variables\n(N=47 prefectures)", fontsize=12, pad=12)
    plt.xticks(rotation=40, ha="right", fontsize=8)
    plt.yticks(rotation=0, fontsize=8)

    out = os.path.join(FIGURES_DIR, "fig7_correlation_heatmap.png")
    fig.savefig(out, dpi=300, bbox_inches="tight")
    plt.close(fig)
    logger.info(f"Fig7保存: {out}")


# ======================================================
# Moran's I
# ======================================================
def run_morans_i():
    try:
        from libpysal.weights import Queen
        from esda.moran import Moran

        gdf_clean = gdf.dropna(subset=["rehab_total_rate"]).copy()
        w = Queen.from_dataframe(gdf_clean)
        w.transform = "r"
        mi = Moran(gdf_clean["rehab_total_rate"], w)
        logger.info(f"Moran's I (rehab_total_rate): I={mi.I:.4f}, p={mi.p_sim:.4f}")

        mi2 = Moran(gdf_clean["hip_fracture_rate"], w)
        logger.info(f"Moran's I (hip_fracture_rate): I={mi2.I:.4f}, p={mi2.p_sim:.4f}")

        return {"rehab": (mi.I, mi.p_sim), "fracture": (mi2.I, mi2.p_sim)}
    except Exception as e:
        logger.warning(f"Moran's I 計算失敗: {e}")
        return None


# ======================================================
# Main
# ======================================================
if __name__ == "__main__":
    logger.info("Phase 5 可視化開始")

    fig1_choropleth_rehab()
    fig2_choropleth_fracture()
    fig3_scatter_main()
    fig4_scatter_h002()
    fig5_scatter_h003()
    fig6_forest_plot()
    fig7_correlation_heatmap()

    morans = run_morans_i()
    if morans:
        logger.info(f"Moran's I 結果: {morans}")

    logger.info("Phase 5 完了 — figures/に7図保存")
    print("Phase 5 完了")
    print(f"出力先: {FIGURES_DIR}")
