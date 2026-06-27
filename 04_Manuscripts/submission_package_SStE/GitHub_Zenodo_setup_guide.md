# GitHub・Zenodo 公開手順ガイド

**プロジェクト**: NDB_XXX_rehabilitation_regional  
**論文**: How Spatial Dependence Alters Ecological Interpretation of Administrative Healthcare Data  
**投稿先**: Spatial and Spatio-temporal Epidemiology  
**作成日**: 2026-06-27

---

## 概要

SStE 投稿に際し、再現性のためにコードと集計データ（都道府県レベルのみ）を GitHub + Zenodo で公開する。  
**NDB 生データは絶対に含めない**（NDB データ利用規約・研究倫理上の禁止事項）。

**現在のリポジトリ:** https://github.com/haruki00430/NDB_XXX_rehabilitation_regional（Private）

---

## Section 1: GitHub リポジトリ準備

### 1-1. リポジトリ名の確認・リネーム検討

現在の名前 `NDB_XXX_rehabilitation_regional` は内部管理向け。論文タイトル・内容に合わせたリネームを **Zenodo 初回 Release 前** に検討する。

| 案 | 長所 | 短所 |
|----|------|------|
| **現状維持** `NDB_XXX_rehabilitation_regional` | 既存 URL を維持、原稿 Data Availability と一致 | 国際読者には分かりにくい |
| `spatial-dependence-ecological-ndb-japan` | 方法論（spatial dependence）を反映 | やや長い |
| `rehabilitation-fracture-spatial-ecology-japan` | 臨床例（rehab–fracture）を反映 | 方法論の主題が弱い |
| **`spatial-ecological-inference-ndb-japan`**（推奨） | 論文の方法論的主題を簡潔に表現 | リネーム作業が必要 |

**推奨:** `spatial-ecological-inference-ndb-japan`  
論文の主題は「リハビリ」より「行政データにおける空間依存と生態学的推論」であるため。

**リネーム手順（GitHub.com 上）:**

1. https://github.com/haruki00430/NDB_XXX_rehabilitation_regional → Settings → General → Repository name
2. 新名称を入力 → **Rename**
3. ローカルの remote URL を更新:

```bash
cd projects/NDB_XXX_rehabilitation_regional
git remote set-url origin https://github.com/haruki00430/spatial-ecological-inference-ndb-japan.git
git remote -v
```

4. 原稿 `Manuscript_SStE.docx` の Data Availability URL を新 URL に更新
5. GitHub は旧 URL から自動リダイレクト（数ヶ月）されるが、原稿・Zenodo メタデータは新 URL を使用すること

> **リネームしない場合:** 現名称のまま Public 化しても投稿上問題なし。Data Availability に記載済み URL と一致させること。

### 1-2. リポジトリの公開（Private → Public）

1. Settings → General → Danger Zone → **Change repository visibility** → Make public
2. 確認ダイアログでリポジトリ名を入力

### 1-3. 公開前チェックリスト

- [ ] `02_Data/raw/` がリポジトリに**含まれていない**（`.gitignore` 確認）
- [ ] `02_Data/interim/` の大容量ファイルが除外されている
- [ ] `.env`、API キー、認証情報が含まれていない
- [ ] `README.md` が英語で最新（論文タイトル・再現手順・引用）
- [ ] `LICENSE` ファイル（MIT または CC-BY-4.0 推奨）
- [ ] `REPRODUCE.md` または `03_Analysis/README.md` に実行順序が記載されている
- [ ] `CITATION.cff`（任意だが Zenodo 連携に有用）

### 1-4. README.md の最小構成（英語）

```markdown
# Spatial Ecological Inference with NDB Open Data (Japan)

Replication code for: Saito H, Ohira T. "How Spatial Dependence Alters Ecological
Interpretation of Administrative Healthcare Data: Lessons From Rehabilitation
Provision and Hip Fracture Surgery Rates in Japan."
*Spatial and Spatio-temporal Epidemiology* (under review, 2026).

## Data sources
- NDB Open Data No.10 (FY2023): https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/0000177182.html
- 2020 Population Census: https://www.stat.go.jp/data/kokusei/2020/

## Reproduction
```bash
pip install -r requirements.txt
python 03_Analysis/analysis/01_extract_rehabilitation_data.py
python 03_Analysis/analysis/02_merge_outcomes.py
python 03_Analysis/analysis/03_regression_spatial.py
python 03_Analysis/analysis/04_visualization.py
```

## License
MIT (code); aggregate data only — no NDB raw files included
```

---

## Section 2: Zenodo アーカイブ

### 2-1. GitHub–Zenodo 連携（推奨）

1. https://zenodo.org にサインイン（GitHub OAuth）
2. Account → **GitHub** タブ
3. リポジトリ（リネーム後の名称）を **ON**
4. Save

### 2-2. DOI 取得（GitHub Release）

1. GitHub → Releases → **Draft a new release**
2. **Tag:** `v1.0.0`
3. **Title:** `v1.0.0 – Initial release for SStE submission`
4. **Description:**

```
Replication code for: Saito H, Ohira T. "How Spatial Dependence Alters Ecological
Interpretation of Administrative Healthcare Data: Lessons From Rehabilitation
Provision and Hip Fracture Surgery Rates in Japan."
Spatial and Spatio-temporal Epidemiology (under review, 2026).

## Contents
- Analysis scripts (03_Analysis/)
- Aggregate prefecture-level datasets (no NDB raw data)
- Manuscript source (04_Manuscripts/)
```

5. **Publish release**
6. 数分後 Zenodo で DOI 発行（例: `10.5281/zenodo.XXXXXXX`）

### 2-3. Zenodo メタデータ

| 項目 | 内容 |
|------|------|
| **Title** | Spatial ecological inference with Japanese NDB Open Data – analysis code |
| **Authors** | Saito, Haruki; Ohira, Tetsuya |
| **Description** | Replication materials for prefecture-level ecological analysis of spatial dependence in administrative healthcare data (N = 47, FY2023). |
| **Keywords** | spatial epidemiology; ecological study; Moran's I; spatial error model; NDB Open Data; Japan |
| **License** | MIT |
| **Related publication** | （受理後に論文 DOI を追記） |

### 2-4. DOI を原稿に反映

Zenodo DOI 発行後:

1. `04_Manuscripts/submission_package_SStE/Manuscript_SStE.docx` の Data Availability を更新
2. プレースホルダ `10.5281/zenodo.XXXXXXX` → 実 DOI
3. 必要なら `prepare_submission_sste.py` の `ZENODO_PLACEHOLDER` を更新して再生成

---

## Section 3: 参考プロジェクトとの比較

| プロジェクト | GitHub リポジトリ | 備考 |
|------------|----------------|------|
| diabetes_unemployment | `NDB_XXX_diabetes_unemployment` | PCD 投稿パッケージ整備済み |
| greenspace_mental_health | `greenspace-mental-health-japan` | CMHJ、Zenodo 連携済み |
| pollen_allergy_v2 | `NDB_pollen_allergy_ecological_japan` | リネーム例 |
| **rehabilitation_regional** | **`NDB_XXX_rehabilitation_regional`** | **要 Public 化・Zenodo DOI** |

---

## タイムライン

| 作業 | タイミング |
|------|-----------|
| リポジトリ名の最終決定 | 投稿前日 |
| `.gitignore` / README 整備 | 投稿前日 |
| Public 化 | 投稿当日 |
| GitHub Release → Zenodo DOI | 投稿当日 |
| Data Availability 更新 | DOI 取得直後 |
| Editorial Manager 投稿 | DOI 確認後 |

---

*作成: 2026-06-27*
