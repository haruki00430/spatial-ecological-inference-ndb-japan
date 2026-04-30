# パイロット適用メモ（NDB_XXX_rehabilitation_regional）

## 適用日

- 2026-04-20

## 適用内容

- `core/manuscript_core.qmd` を正本として配置。
- `variants/submission.qmd` と `variants/preprint.qmd` を作成。
- `includes/` に以下の差分テンプレートを作成。
  - `preprint_disclaimer.qmd`
  - `data_transparency.qmd`
  - `submission_journal_notes.qmd`
- `quarto/` に投稿版・プレプリント版の設定ファイルを分離。
- `outputs/submission` と `outputs/preprint` を分離。

## タイトル固定ルール

- 正本タイトルは `core/manuscript_core.qmd` を基準とし、派生版で書き換えない。
- プレプリント版で必要な差分はタイトル変更ではなく注記ブロックで付与する。

## レンダリング例

```powershell
quarto render "variants/submission.qmd" --metadata-file "quarto/_quarto_submission.yml"
quarto render "variants/preprint.qmd" --metadata-file "quarto/_quarto_preprint.yml"
```
