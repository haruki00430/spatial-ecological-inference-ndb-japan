# Editorial Manager アップロード順序ガイド
# README: Upload Order for Editorial Manager (Spatial and Spatio-temporal Epidemiology)

**投稿ポータル**: https://www.editorialmanager.com/sste/  
**Article Type**: Original Research Article  
**準備日**: 2026-06-27

---

## このフォルダの全ファイル一覧

| ファイル | 説明 | Editorial Manager 分類 |
|---------|------|----------------------|
| `Manuscript_SStE.docx` | **本文（メイン）** Highlights・Tables・Figure legends 含む | Manuscript |
| `CoverLetter_SStE.md` | カバーレター（DOCX変換可） | Cover Letter |
| `Highlights_SStE.docx` | ハイライト（必須・5項目・85文字以内） | Highlights |
| `GraphicalAbstract_SStE.png` | **Graphical Abstract（必須）** | Graphical Abstract |
| `Figure1_SStE.png` | Fig1: リハビリ算定率 choropleth | Figure |
| `Figure2_SStE.png` | Fig2: 大腿骨骨折手術率 choropleth | Figure |
| `Figure3_SStE.png` | Fig3: 散布図（主要 association） | Figure |
| `Figure4_SStE.png` | Fig4: 感度分析 Forest plot | Figure |
| `Figure5_SStE.png` | Fig5: 相関ヒートマップ | Figure |
| `SuppFigureS1_SStE.png` | 補足Fig S1: H002 散布図 | Supplementary Material |
| `SuppFigureS2_SStE.png` | 補足Fig S2: H003 散布図 | Supplementary Material |
| `TitlePage_SStE.md` | 著者情報（EM入力用） | — |
| `COI_Statement_SStE.md` | 利益相反宣言（参考） | — |
| `submission_workflow_SStE.md` | 投稿手順書（詳細） | — |
| `GitHub_Zenodo_setup_guide.md` | コード公開手順 | — |
| `Guide for authors ... Elsevier.pdf` | 投稿規定（要再配置・下記参照） | — |

---

## アップロード順序（Editorial Manager 推奨）

### Step 1: Cover Letter
- `CoverLetter_SStE.md` の内容をテキストボックスに貼り付け、または DOCX に変換してアップロード
- EM分類: **Cover Letter**

### Step 2: Manuscript（本文）
- `Manuscript_SStE.docx`（**図なし版** — キャプションのみ。Figure PNG は Step 5–6 で別アップロード）
- EM分類: **Manuscript**
- 本文に Highlights・Abstract・Tables 1–2・Figure Legends を含む

### Step 3: Highlights（必須）
- `Highlights_SStE.docx`（または `Highlights_SStE.txt` から5行をコピー）
- EM分類: **Highlights**

### Step 4: Graphical Abstract（必須）
- `GraphicalAbstract_SStE.png`
- EM分類: **Graphical Abstract**
- 最低解像度: 531 × 1328 pixels (h × w) 以上

### Step 5: Main Figures（5点）

| 順序 | ファイル | Figure 番号 | EM分類 |
|------|---------|------------|-------|
| 1 | `Figure1_SStE.png` | Figure 1 | Figure |
| 2 | `Figure2_SStE.png` | Figure 2 | Figure |
| 3 | `Figure3_SStE.png` | Figure 3 | Figure |
| 4 | `Figure4_SStE.png` | Figure 4 | Figure |
| 5 | `Figure5_SStE.png` | Figure 5 | Figure |

### Step 6: Supplementary Material
- `SuppFigureS1_SStE.png` — Supplementary Figure S1
- `SuppFigureS2_SStE.png` — Supplementary Figure S2
- EM分類: **Supplementary Material**
- 補足 Table S1 は本文内に記載済み（必要に応じ PDF 化）

---

## SStE 投稿規定チェックリスト（最終確認）

### 本文内容
- [x] Abstract ≤250語（現在235語） ✓
- [x] Abstract 構造: Background / Methods / Results / Conclusions ✓
- [x] Keywords: 6語 ✓
- [x] Highlights: 5項目 × 各≤85文字 ✓
- [x] Graphical Abstract: 別ファイル作成済み ✓
- [x] Main Figures: 5点 ✓
- [x] Supplementary Figures: 2点 ✓
- [x] References: Vancouver 番号形式 ✓
- [x] Ethics Statement 記載済み ✓
- [x] Competing Interests 記載済み ✓
- [x] Funding 記載済み ✓
- [x] CRediT Author Contributions 記載済み ✓
- [x] AI Disclosure 記載済み ✓
- [x] Data Availability（GitHub + Zenodo プレースホルダ）記載済み ✓
- [x] **本文語数確認済み** — Introduction–Conclusions **2,430語**（Abstract 235語）
- [x] **メタデータ確認済み** — author / lastModifiedBy / title 等は空
- [x] **図の二重掲載リスク解消** — DOCX から埋め込み図7点削除、PNG は別アップロード

### 著者情報（EM入力）

| 著者 | 所属 | ORCID | 役割 |
|------|------|-------|------|
| Haruki Saito | Fukushima Medical University | 0009-0009-7890-6068 | Corresponding |
| Tetsuya Ohira | Fukushima Medical University | 0000-0003-4532-7165 | Co-author |

**通信著者メール**: m211039@fmu.ac.jp

---

## 注意事項

### 投稿規定 PDF について
配置済みの `Guide for authors ... Elsevier.pdf` は **ファイルサイズ異常（リンク切れの可能性）** のため、ScienceDirect から再ダウンロードして上書きすることを推奨します。参照用に `SStE_guide_for_authors_downloaded.pdf`（Elsevier 共通テンプレート）も同梱していますが、**正本は ScienceDirect の SStE 専用 Guide for Authors** です。

### 投稿直前の確認
1. Word で `Manuscript_SStE.docx` を開き、ファイル → 情報 → ドキュメントの検査でメタデータを削除
2. Zenodo DOI 取得後、Data Availability のプレースホルダを実 DOI に更新
3. Graphical Abstract の視認性を 5×13 cm 相当で確認

---

*作成: 2026-06-27*
