# DEATH_GAME — シナリオ管理

オリジナル推理ドラマのシナリオ原稿を作品別に管理するリポジトリです。

## 作品一覧

| フォルダ | 作品 | 収録 |
| --- | --- | --- |
| [01_REPORT0](scenarios/01_REPORT0/) | REPORT:0 — 死亡予告 | 全8話・第7稿 |
| [02_Midnight](scenarios/02_Midnight/) | 午前零時の不在証明 | 全8話・改訂版 |
| [03_KuonGama](scenarios/03_KuonGama/) | 報告書：久遠窯 | 全8話 |
| [04_24Minutes](scenarios/04_24Minutes/) | 24分のタイムパラドックス | 全4話 |

## 管理ルール

- 各フォルダの `scenario.txt` は元の添付シナリオを改変せずに保管しています。
- 新しい改訂稿は、元原稿を上書きせず版番号付きの新規ファイルとして追加してください。
- レビュー報告書や人物相関図などは、必要に応じて各作品フォルダ内で管理できます。
- 原稿は制作資料であり、最終校了・映像化承認済みとは限りません。

## レビュー報告書

作品ごとの `reviews/` フォルダに、複数の独立したレビュー結果を原文のまま区別して保存しています。

- [REPORT:0 レビュー（3件）](scenarios/01_REPORT0/reviews/)
- [午前零時の不在証明 レビュー（2件）](scenarios/02_Midnight/reviews/)
- [報告書：久遠窯 レビュー（4件）](scenarios/03_KuonGama/reviews/)
- [24分のタイムパラドックス レビュー（3件）](scenarios/04_24Minutes/reviews/)

久遠窯の `additional_review_from_docx.md` は、Word原稿から本文を抽出した閲覧用テキストであり、元のWordレイアウトは含みません。レビューごとに評価が異なる場合も、統合・上書きせず原文を保持します。
