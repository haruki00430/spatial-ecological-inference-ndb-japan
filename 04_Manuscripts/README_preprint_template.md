# 投稿版/プレプリント版テンプレート運用ガイド

## タイトル運用方針

- `core/manuscript_core.qmd` のタイトルは変更しない。
- `variants/submission.qmd` と `variants/preprint.qmd` は同一タイトルを継承する。
- プレプリントでの差分はタイトル書換えではなく、注記ブロックで表現する。

## 単一正本

- 本文は `core/manuscript_core.qmd` を正本として管理する。
- 配布先ごとの差分は `variants` と `includes` のみで扱う。

## レンダリング例

```powershell
quarto render "variants/submission.qmd" --output-dir "outputs/submission"
quarto render "variants/preprint.qmd" --output-dir "outputs/preprint"
```

または以下を実行する。

```powershell
powershell -ExecutionPolicy Bypass -File ".\render_variants.ps1"
```

## 公開前チェック

- 主結果（効果量、CI、p値など）が版間で一致していることを確認する。
- `Not peer reviewed` 注記がプレプリント版にのみ存在することを確認する。
- 出力先が `outputs/submission` と `outputs/preprint` で分離されていることを確認する。
- `core/manuscript_core.qmd` のタイトルが不変であることを確認する。
