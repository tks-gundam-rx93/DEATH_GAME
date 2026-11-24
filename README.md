# DEATH_GAME — シナリオ管理

オリジナル推理ドラマのシナリオ原稿を作品別に管理するリポジトリです。

## 作品一覧

| フォルダ | 作品 | 収録 |
| --- | --- | --- |
| [01_REPORT0](scenarios/01_REPORT0/) | REPORT:0 — 死亡予告 | 全8話・第9稿（第7稿・第8稿も保存） |
| [02_Midnight](scenarios/02_Midnight/) | 午前零時の不在証明 | 全8話・[元稿](scenarios/02_Midnight/scenario.txt)／[レビュー反映版 v2.0](scenarios/02_Midnight/scenario_v2.txt) |
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
- [午前零時の不在証明 レビュー（3件）](scenarios/02_Midnight/reviews/)
- [報告書：久遠窯 レビュー（4件）](scenarios/03_KuonGama/reviews/)
- [24分のタイムパラドックス レビュー（3件）](scenarios/04_24Minutes/reviews/)

久遠窯の `additional_review_from_docx.md` は、Word原稿から本文を抽出した閲覧用テキストであり、元のWordレイアウトは含みません。レビューごとに評価が異なる場合も、統合・上書きせず原文を保持します。

### REPORT:0 最新改訂稿

- **最新**：[第9稿（レビュー3件を反映）](scenarios/01_REPORT0/scenario_v9_all_reviews_applied.txt)
- **原本**：[第7稿](scenarios/01_REPORT0/scenario.txt)
- **レビュー資料**：[3AI合議レビュー](scenarios/01_REPORT0/reviews/3AI_council_review_2026-11-22.md)、[TRE-THESAURUSレビュー](scenarios/01_REPORT0/reviews/TRE_THESAURUS_review.md)、[詳細レビュー](scenarios/01_REPORT0/reviews/detailed_scenario_review.md)
- 対応：レビューの重大4項目を含む G-01〜G-20 を改訂監査票として追記。第8稿のドラフトPR #1は取り下げ（クローズ、未マージ）。

## 第1話 映像制作（制作中）

- [制作計画・生成タスク台帳](scenarios/01_REPORT0/production/EP01_PRODUCTION_PLAN.md)
- [全43カット・510秒のショット表](scenarios/01_REPORT0/production/EP01_SHOTLIST.csv)
- [01-01日本語仮音声の台詞とキュー](scenarios/01_REPORT0/production/EP01_SC01_VOICE_CUES.md)

第1話の初期15秒の動画生成と、01-01の多話者日本語仮音声を開始済み。最終的な本編編集・検収は未完了です。

### 第1話セリフ校正（Owner確認待ち）

- [全文：セリフ校正案](scenarios/01_REPORT0/production/EP01_DIALOGUE_REVISED_DRAFT.md)
- [39発話・原文／修正案比較表](scenarios/01_REPORT0/production/EP01_DIALOGUE_MASTER.csv)
- [TTS入力台本（「トレ、テサウルス」の区切り指定）](scenarios/01_REPORT0/production/EP01_TTS_SCRIPT.csv)
- [変更履歴／検収条件](scenarios/01_REPORT0/production/EP01_DIALOGUE_FIX_LOG.md)

第9稿の原本を保全し、まずOwnerが修正案を確認する運用です。

## 読み上げ専用台本（漢字なし）

[作品別の読み上げ台本一覧](scenarios/TTS_INDEX.md)

画面に表示する原稿は変更せず、音声に渡すセリフだけを仮名に置き換えて管理しています。現在の収録範囲：REPORT:0第1話、午前零時の不在証明第1話、久遠窯第1話、24分のタイムパラドックス全4話。その他の話数は未作成です。

### 第1話・2026-11-24 映像／音声制作状況

- [最新制作レポート（音声付き91.366秒ダイジェスト生成・510秒本編の未完了工程）](scenarios/01_REPORT0/production/EP01_REMAINING_WORK_20261124.md)
- 日本語音声付きダイジェスト生成タスク：`b24157c1-1d14-49f3-abac-d819b653c96e`（1280×720・音声あり）。Runwayの生成ビューアーで視聴可。
- 字幕付きアニマティックは510秒。全39セリフの日本語音声は別資産として生成済みだが、ローカルMP4への合成は未完了。ダイジェストを完成本編と誤認しないこと。

- **最新（2026-11-24）**：全43カット・510秒の字幕なしアニマティックと仮名字幕付きレビュー版を再構築。音声付き全7シーンの実写風ダイジェストは **111.526秒** へ更新（Runwayタスク `56b9e879-455a-48ea-b008-928e3f3dc28c`）。全39セリフの新しい推定音声キューは [制作フォルダのCSV](scenarios/01_REPORT0/production/EP01_TTS_ESTIMATED_TIMING.csv) に記録。**全8分30秒の日本語音声入り完成映像は未完成**。
