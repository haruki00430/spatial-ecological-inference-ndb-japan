# 他プロジェクト横展開チェックリスト

## 対象範囲

`04_Manuscripts/` 配下に `Manuscript_<project>.qmd` 相当の原稿を持つプロジェクトを対象とする。

## Step 1: 標準構成の作成

- `core/`, `variants/`, `includes/`, `quarto/`, `outputs/submission/`, `outputs/preprint/` を作成する。
- 既存原稿の本文を `core/manuscript_core.qmd` に移行する。
- `core/manuscript_core.qmd` のタイトルは変更しない。

## Step 2: 派生ラッパーの作成

- `variants/submission.qmd` を作成し、`../core/manuscript_core.qmd` を include する。
- `variants/preprint.qmd` を作成し、以下を include する。
  - `../includes/preprint_disclaimer.qmd`
  - `../core/manuscript_core.qmd`
  - `../includes/data_transparency.qmd`

## Step 3: 出力先とレンダリング設定

- 投稿版出力は `outputs/submission` に固定する。
- プレプリント版出力は `outputs/preprint` に固定する。
- メタデータ設定ファイルを分離する。
  - `quarto/_quarto_submission.yml`
  - `quarto/_quarto_preprint.yml`

## Step 4: 公開前QA

- 本文整合: 投稿版とプレプリント版で意図しない本文差分がない。
- 数値整合: 効果量、CI、p値、モデル適合度が一致する。
- 安全表示: プレプリント版に未査読注記がある。
- タイトル整合: 派生版が正本タイトルを書き換えていない。
- 参照整合: 引用番号と図表番号の順序が安定している。

## Step 5: 推奨コマンド

```powershell
quarto render "variants/submission.qmd" --output-dir "outputs/submission"
quarto render "variants/preprint.qmd" --output-dir "outputs/preprint"
```

または:

```powershell
powershell -ExecutionPolicy Bypass -File ".\render_variants.ps1"
```
