# GitHub・Zenodo 公開手順ガイド

**プロジェクト**: spatial-ecological-inference-ndb-japan  
**論文**: How Spatial Dependence Alters Ecological Interpretation of Administrative Healthcare Data  
**投稿先**: Spatial and Spatio-temporal Epidemiology  
**最終更新**: 2026-06-27

---

## 完了済みステータス

| 作業 | 状態 |
|------|------|
| GitHub リネーム → `spatial-ecological-inference-ndb-japan` | ✅ 完了 |
| Public 化 | ✅ 完了 |
| Zenodo–GitHub 連携 ON | ✅ 完了（ユーザー設定済み） |
| 公開用 README / REPRODUCE / DATA_SOURCES / LICENSE | ✅ 完了 |
| `data/release/analysis_dataset_prefecture_n47.csv` | ✅ コミット済み |
| GitHub Release `v1.0.1` | ✅ 完了 |
| Zenodo DOI `10.5281/zenodo.20951654` | ✅ 完了 |
| 原稿 Data Availability 反映 | ✅ 完了 |

**リポジトリ URL:** https://github.com/haruki00430/spatial-ecological-inference-ndb-japan

---

## Zenodo DOI 取得手順（Release 後）

1. GitHub で Release `v1.0.1` を公開（Zenodo 連携 ON 後の初回 Release）
2. 数分待ち、Zenodo の Repositories ページで Release が表示されることを確認
3. DOI を取得（例: `10.5281/zenodo.20951654`）
4. 以下を実行して原稿・ドキュメント一括更新:

```bash
python 04_Manuscripts/update_zenodo_doi.py 10.5281/zenodo.20951654
python 04_Manuscripts/prepare_submission_sste.py
```

---

## 引用例

```
Saito H, Ohira T. How Spatial Dependence Alters Ecological Interpretation...
GitHub: https://github.com/haruki00430/spatial-ecological-inference-ndb-japan
Zenodo: https://doi.org/10.5281/zenodo.20951654
```

---

*詳細な初回設定手順は diabetes_unemployment プロジェクトの `GitHub_Zenodo_setup_guide.md` を参照。*
