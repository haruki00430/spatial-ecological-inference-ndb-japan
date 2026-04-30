# Validation Report — Phase 6: Final Review

**Project**: NDB_XXX_rehabilitation_regional  
**Date**: 2026-04-15  
**Validator**: Claude Code (Validator Skill)  
**Overall Status**: ✅ APPROVED with WARNING (Level 1-2 issues only)

---

## 1. Security Audit

| Check | Result | Detail |
|---|---|---|
| `02_Data/raw/` 変更なし | ✅ PASS | `git diff 02_Data/raw/` = 0 chars (変更なし) |
| 実データAI送信禁止 | ✅ PASS | `print(df.head(N))` / `plt.show()` パターン未検出 |
| `.gitignore` 遵守 | ✅ PASS | `.obsidian/`, `.claude/settings.local.json`, `02_Data/raw/` すべてカバー |
| `.claude/` Git管理 | ⚠️ WARNING | `.claude/` 一部ファイル（README.md, skills等）がGit管理されている。NDB_Research_Hub のスキル・エージェント定義は共有設計のため意図的なもの。**プロジェクト固有の `.claude/` は含まれていないため許容範囲。** |

---

## 2. Reproducibility（再現性）

| Check | Result | Detail |
|---|---|---|
| スクリプト番号順保存 | ✅ PASS | `01_` `02_` `03_` `04_` の順に4スクリプト |
| ロガー初期化（全スクリプト） | ✅ PASS | `setup_logger(__name__, log_file=...)` 全4スクリプトに実装 |
| ログ記録（行数変化記録） | ✅ PASS | phase1: 71行, phase2: 11行, phase3/4: 110行, phase5: 7行 |
| 中間ファイル保存 | ✅ PASS | `rehabilitation_prefecture.csv`, `fracture_outcome.csv`, `analysis_dataset.csv` |
| 乱数シード固定 | N/A | Bootstrap・Monte Carloは使用していない（OLS回帰のみ） |
| スクリプト構文エラーなし | ✅ PASS | 全4スクリプトが `py_compile` 通過 |

### スクリプト配置場所の指摘
⚠️ **Level 1**: スクリプトが `03_Analysis/analysis/` に保存されている（Validator チェックリストの期待する `03_Analysis/scripts/` とは異なる）。機能的な問題はないが、標準ディレクトリ規約との乖離あり。

---

## 3. Data Quality（Phase 1: ETL）

| Check | Result | Detail |
|---|---|---|
| Excel読み込み方式 | ✅ PASS | `header=None` + 行3から手動マッピング（ワイド形式対応） |
| `clean_numeric()` | N/A | ワイド形式のため手動パース。`pd.to_numeric(..., errors='coerce')` で同等処理実施 |
| 欠損値率 | ✅ PASS | 47都道府県が揃っている（欠損なし） |
| データ型 | ✅ PASS | 算定回数→float64, 都道府県名→str |
| 出力行数 | ✅ PASS | 47行（全都道府県） |

**注意**: H_リハビリテーションExcelは通常の `header=[2,3]` パターン（MultiIndex）ではなくワイド形式。本プロジェクトはこれを正しく検出し独自パーサーを実装した。

---

## 4. Statistical Validity（Phase 2-3）

| Check | Result | Detail |
|---|---|---|
| VIF < 10 | ✅ PASS | 全3曝露: aging=1.66, pop_density=1.65, exposure≈1.0（最大でも1.68） |
| Shapiro-Wilk 残差正規性 | ✅ PASS | stat=0.9837, p=0.7459 → 正規性棄却せず |
| サンプルサイズ十分性 | ✅ PASS | N=47, 説明変数3個 → N/covariate = 15.7（>10） |
| 感度分析6仕様 | ✅ PASS | Spec1-6全仕様が実装・実行済み |
| Moran's I | ✅ PASS | rehab_total: I=0.547, p=0.001; hip_fracture: I=0.563, p=0.001 |
| LM検定によるモデル選択 | ⚠️ **Level 2** | LM test（Lagrange Multiplier）未実施。Moran's I > 0.54の強い空間自己相関があるにもかかわらず、OLS のみで空間ラグ/誤差モデルを検討していない。**Discussionで限界として言及済みだが、補足解析として空間回帰モデルの追加を推奨。** |

---

## 5. Figure Quality（Phase 4）

| Check | Result | Detail |
|---|---|---|
| `set_japanese_font()` 呼出し | ✅ PASS | スクリプト冒頭（matplotlib より前）に配置 |
| dpi=300 | ✅ PASS | 全7図で `dpi=300, bbox_inches="tight"` |
| 保存先 | ✅ PASS | `03_Analysis/results/figures/` に全7図保存 |
| 図の数 | ✅ PASS | Fig1-7の7図揃い |
| 透かし | N/A | 実データ使用のため透かし不要 |

---

## 6. Manuscript Quality（Phase 5-6）

| Check | Result | Detail |
|---|---|---|
| Abstract 引用番号なし | ✅ PASS | Abstract内に `[@...]` パターンなし |
| 参考文献初登場順（Vancouver） | ✅ PASS | Quartoが自動処理。Introduction冒頭から順に引用 |
| 参考文献件数 | ✅ PASS | references.bib に21件 |
| DOCX出力 | ✅ PASS | `Manuscript_rehabilitation_regional.docx` 生成済み |
| HTML出力 | ✅ PASS | `Manuscript_rehabilitation_regional.html` 生成済み |
| vancouver.csl 添付 | ✅ PASS | `04_Manuscripts/vancouver.csl` 配置済み |
| AI_USE_DISCLOSURE.md | ✅ PASS | 配置済み |

### 図番号登場順序
⚠️ **Level 2**: 本文中の図参照順序が非連続。

- Results: Correlation Analysis 節 → **Figure 7** が最初に参照（p.5）
- Results: Regression Analysis 節 → **Figure 3**, **Figure 6** が参照（p.5）
- Figure Captions（末尾）: Fig1→7の順で列挙

Figure 1, 2, 4, 5 は本文中で明示的に参照されておらず、Figure 7 が Figure 3 より先に参照されている。Vancouver スタイルの図番号規則（初登場順）への対応が推奨される。

**修正案**:
- Descriptive Statistics 節の先頭に「都道府県分布は Figure 1（リハビリ率）および Figure 2（骨折率）に示す」を追加
- Correlation Analysis で Figure 7 を最後に移動するか、図番号を振り直す

---

## 7. Issues Detected

| Level | 件数 | 内容 |
|---|---|---|
| Level 4（致命的） | 0 | — |
| Level 3（重大） | 0 | — |
| Level 2（中程度） | 2 | ① 空間回帰モデル（LM検定）未実施、② 図番号登場順序が非連続 |
| Level 1（軽微） | 1 | ③ スクリプト保存先が `analysis/` で `scripts/` でない |

---

## 8. Recommendations（修正推奨事項）

### ⭐ 推奨（投稿前に対応）

**R1 [Level 2]: 図番号の本文参照順序を修正**  
Figure 1, 2 を Descriptive Statistics 節で明示的に参照し、図の登場順が Figure 1 → 2 → 3 → ... → 7 の順になるよう修正する。

```markdown
# Descriptive Statistics 節に追記
Geographic distribution of rehabilitation total rate and hip fracture rate 
by prefecture are shown in **Figure 1** and **Figure 2**, respectively.
```

**R2 [Level 2]: 補足として空間回帰モデルを追加検討**  
Moran's I > 0.54 の強い空間自己相関が確認されており、OLS の独立性仮定が違反している可能性がある。査読時の指摘リスクを下げるため、Spatial Error Model または Spatial Lag Model の補足解析を追加することを推奨する（libpysal/spreg で実装可能）。

### 任意（対応不要）

**R3 [Level 1]**: スクリプトを `03_Analysis/scripts/` に移動するか、`README.md` に `03_Analysis/analysis/` が実行フォルダである旨を明記する。

---

## 9. Approval Status

```
┌─────────────────────────────────────────────────────┐
│  ✅ APPROVED with WARNING                           │
│                                                     │
│  致命的・重大な問題なし。                           │
│  Level 2 x2 (図番号順序、空間回帰未実施) を         │
│  投稿前に対応することを強く推奨する。               │
│                                                     │
│  投稿ターゲット:                                    │
│  Archives of Physical Medicine and Rehabilitation   │
│  (IF ~4.0) / Journal of Epidemiology (IF ~2.9)     │
└─────────────────────────────────────────────────────┘
```

---

*Validator: Claude Code (claude-sonnet-4-6) | 2026-04-15*
