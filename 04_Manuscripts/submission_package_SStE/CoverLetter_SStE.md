# Cover Letter – Spatial and Spatio-temporal Epidemiology

**Date**: 2026-06-27

**To**:  
Professor Russell S. Kirby, PhD, MS  
Editor-in-Chief  
*Spatial and Spatio-temporal Epidemiology*

---

Dear Professor Kirby,

We respectfully submit the original research article entitled **"How Spatial Dependence Alters Ecological Interpretation of Administrative Healthcare Data: Lessons From Rehabilitation Provision and Hip Fracture Surgery Rates in Japan"** for consideration for publication in *Spatial and Spatio-temporal Epidemiology*.

**Why this paper fits *Spatial and Spatio-temporal Epidemiology*:**  
Ecological analyses of administrative healthcare data are increasingly used for health services and policy research, yet spatial dependence is often treated as a secondary concern. Using Japan's 47 prefectures and NDB Open Data No.10 (FY2023), we provide an empirical demonstration of how Global Moran's I, Lagrange Multiplier diagnostics, and spatial econometric models (Spatial Error Model and Spatial Lag Model) can materially change the interpretation of an exposure–outcome association. The clinical pairing—rehabilitation claim rates and hip fracture surgery rates—is policy-relevant and measurable in open claims data, but the primary contribution is methodological: spatial diagnostics as a routine component of ecological inference.

**Key findings:**  
Rehabilitation claim rates varied 6.8-fold across prefectures. In adjusted OLS models, rehabilitation rate was positively associated with hip fracture surgery rate (β = 0.0005; p < 0.001; robust across six sensitivity specifications). Both variables exhibited strong positive spatial autocorrelation (Moran's I > 0.54, p = 0.001). LM tests favored a Spatial Error Model (ΔAIC = −16.6 vs OLS; λ = 0.671, p < 0.001), after which the rehabilitation coefficient was attenuated and no longer statistically significant (β = 0.000164, p = 0.130). Interpretation also differed under the Spatial Lag Model, underscoring that model choice matters.

**Novelty:**  
To our knowledge, this is among the first prefecture-level studies to show that a statistically robust OLS ecological association between rehabilitation provision and fracture-related surgery rates can be substantially explained by spatially structured residual dependence rather than a direct ecological relationship. The paper offers a reproducible workflow (Python; libpysal/esda) applicable to other administrative open-data settings.

**Ethics and data:**  
This study used only publicly available, aggregate NDB Open Data with no individual-level records. Ethics committee approval was not required.

**Data and code availability:**  
Analysis scripts and aggregate datasets are archived at https://github.com/haruki00430/NDB_XXX_rehabilitation_regional (Zenodo DOI to be assigned upon release).

**Authorship and conflicts:**  
All authors approved the manuscript and declare no competing interests. This work received no specific funding.

We confirm that this manuscript has not been published previously and is not under consideration elsewhere. We suggest the following reviewers (optional):

- Researchers with expertise in spatial econometrics applied to health administrative data
- Researchers studying geographic variation in rehabilitation or fracture care in Japan or comparable universal-coverage systems

We look forward to your consideration.

Sincerely,

**Haruki Saito, MD**  
Department of Epidemiology  
Fukushima Medical University School of Medicine  
1 Hikarigaoka, Fukushima-shi, Fukushima 960-1295, Japan  
Email: haruki00430@gmail.com  
ORCID: 0009-0009-7890-6068

**Tetsuya Ohira, MD, PhD**  
Department of Epidemiology  
Fukushima Medical University School of Medicine  
ORCID: 0000-0003-4532-7165

*On behalf of all authors*
