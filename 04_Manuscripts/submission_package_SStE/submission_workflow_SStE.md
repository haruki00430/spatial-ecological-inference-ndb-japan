# SStE 投稿ワークフロー・チェックリスト

**論文:** How Spatial Dependence Alters Ecological Interpretation of Administrative Healthcare Data: Lessons From Rehabilitation Provision and Hip Fracture Surgery Rates in Japan  
**投稿先:** Spatial and Spatio-temporal Epidemiology (Elsevier)  
**投稿日目標:** 2026-06-27  
**作成日:** 2026-06-27

---

## 1. ジャーナル基本情報

| 項目 | 内容 |
|------|------|
| ジャーナル名 | Spatial and Spatio-temporal Epidemiology |
| 出版社 | Elsevier |
| ISSN | 1877-5845 |
| 投稿システム | Editorial Manager |
| 投稿 URL | https://www.editorialmanager.com/sste/ |
| Editor-in-Chief | Russell S. Kirby, PhD, MS (University of South Florida) |
| 査読方式 | Single anonymized review（Elsevier 標準） |
| 引用スタイル | 番号付き Vancouver 形式（原稿準拠） |
| APC（Open Access 選択時） | USD 3,300（2026年時点・投稿時に確認） |
| 論文種別 | Original Research Article |

---

## 2. 投稿ファイル一覧

本フォルダ（`submission_package_SStE/`）に収録されているファイル：

| ファイル名 | 用途 | 状態 |
|-----------|------|------|
| `Manuscript_SStE.docx` | **主原稿（SStE要件修正済み）** | ✅ 完成 |
| `Highlights_SStE.docx` / `.txt` | ハイライト（必須） | ✅ 完成 |
| `GraphicalAbstract_SStE.png` | Graphical Abstract（必須） | ✅ 完成 |
| `CoverLetter_SStE.md` | カバーレター | ✅ 完成 |
| `TitlePage_SStE.md` | 著者情報（EM入力用） | ✅ 完成 |
| `COI_Statement_SStE.md` | 利益相反宣言 | ✅ 完成 |
| `Figure1_SStE.png` 〜 `Figure5_SStE.png` | メイン図5点 | ✅ 完成 |
| `SuppFigureS1_SStE.png`, `SuppFigureS2_SStE.png` | 補足図2点 | ✅ 完成 |
| `README_UPLOAD_ORDER.md` | アップロード順序 | ✅ 完成 |
| `GitHub_Zenodo_setup_guide.md` | コード公開手順 | ✅ 完成 |

### 関連ソースファイル（フォルダ外）

| ファイル名 | 用途 | 備考 |
|-----------|------|------|
| `../How_Spatial_Dependence_Alters_Ecological_Interpretation_20260619.docx` | 原稿ベース（変更前） | 正本を保護 |
| `../Manuscript_rehabilitation_regional.qmd` | Quarto ソース | 将来の再レンダリング用 |
| `../prepare_submission_sste.py` | 投稿パッケージ生成スクリプト | 再実行可 |

---

## 3. 投稿規定に基づく DOCX 修正サマリー

| 項目 | 変更内容 |
|------|---------|
| 著者情報 | 所属・通信著者・ORCID・Running title を追加 |
| Highlights | 本文 Abstract 直前に5項目挿入 + 別ファイル作成 |
| Keywords | 8語 → **6語**（Elsevier 上限準拠） |
| Authors' Contributions | CRediT 形式に著者名を反映 |
| Data Availability | GitHub URL + Zenodo DOI `10.5281/zenodo.20951654` |
| 図構成 | メイン5点 + 補足2点（原稿20260619版に準拠） |

---

## 4. 投稿前チェックリスト

### 4-1. コンテンツ確認

- [x] タイトル完全記載
- [x] Running title ≤80文字
- [x] Abstract ≤250語（235語）
- [x] Keywords 6語
- [x] Highlights 5項目 × 各≤85文字
- [x] Graphical Abstract 作成（531×1328 px 以上）
- [ ] 全文語数（References・Tables・Figure legends 除く）— Word で最終確認
- [x] 図5点・表2点の番号・キャプション一致

### 4-2. SStE / Elsevier 必須記載事項

- [x] Ethics Statement
- [x] Data Availability（GitHub + Zenodo）
- [x] Competing Interests
- [x] Funding
- [x] CRediT Author Contributions
- [x] AI 利用開示

### 4-3. 図ファイル

- [x] PNG 300 dpi 相当（choropleth / scatter / forest）
- [ ] 必要に応じ TIFF 変換（Elsevier Artwork Guidelines 参照）
- [x] 図は本文に埋め込まず別ファイルアップロード

### 4-4. コード公開

- [x] GitHub 公開前チェック（`.gitignore` で raw データ除外確認）
- [x] GitHub Release `v1.0.1` → Zenodo DOI `10.5281/zenodo.20951654`
- [x] Data Availability の DOI 反映済み

---

## 5. Editorial Manager 投稿手順

1. https://www.editorialmanager.com/sste/ にログイン（または新規登録）
2. **Submit New Manuscript**
3. Article Type: `Original Research Article`（または Full Length Article）
4. Title / Abstract / Keywords を `TitlePage_SStE.md` および `Manuscript_SStE.docx` から入力
5. 著者情報を登録（ORCID 連携推奨）
6. ファイルを `README_UPLOAD_ORDER.md` の順序でアップロード
7. Declarations フォーム（Ethics, COI, Funding, Data）を入力
8. **Build PDF for Approval** → プレビュー確認 → Submit

---

## 6. SStE 投稿規定の重要ポイント（要約）

| 項目 | SStE / Elsevier の要件 |
|------|----------------------|
| Highlights | **必須** — 3〜5項目、各85文字以内（スペース含む） |
| Graphical Abstract | **必須** — 別ファイル、最低 531×1328 px (h×w) |
| Abstract | 250語以内、References なし |
| Keywords | 最大6語 |
| Cover letter | 必須 |
| 査読 | Single anonymized（著者名は原稿に記載可） |
| CRediT | Author Contributions 推奨/必須 |
| Data Availability | 必須 |
| AI 開示 | 必須（References 前の専用セクション） |
| 補足資料 | 図・表は Supplementary Material として別アップロード可 |

> **注:** 配置済み PDF（`Guide for authors ... Elsevier.pdf`）が破損している場合、ScienceDirect の [Guide for authors](https://www.sciencedirect.com/journal/spatial-and-spatio-temporal-epidemiology/publish/guide-for-authors) から再取得してください。

---

## 7. 投稿後の管理

| ステータス | 目安 | 対応 |
|-----------|------|------|
| Under Review | 数ヶ月（Elsevier 平均: first decision ~109日） | 待機 |
| Revision | 受領後 | 査読コメント対応 |
| Accepted | — | 最終校・APC/OA 選択 |
| 受理後 | — | Zenodo DOI を正式版に反映 |

---

*作成: 2026-06-27*
