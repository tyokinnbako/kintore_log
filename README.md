# kintore_log

筋トレ記録から、部位ごとのバランスと回復日数を出すコマンドです。

## 動作環境

- Ubuntu
- Python 3.12

## インストール

    $ git clone https://github.com/tyokinnbako/kintore_log.git
    $ cd kintore_log

インストールは不要です。そのまま `./kintore_log` で実行できます。

## 使い方

    $ cat examples/workouts.txt | ./kintore_log

## 入力

1行が1回のトレーニングで、日付、種目名、部位、セット数をスペースで区切って書きます。

    2026-11-20 bench_press chest 3

- 日付: トレーニングした日
- 種目名: メモ用で、集計には使いません
- 部位: chest、back、shoulders、arms、legs、abs のいずれか
- セット数: セット数（数字）

## 出力

    balance
    chest 7.0 53.8
    back 3.0 23.1
    shoulders 0.0 0.0
    arms 0.0 0.0
    legs 3.0 23.1
    abs 0.0 0.0
    low shoulders
    recovery
    chest 0 休め
    back 2 OK
    shoulders - 未記録
    arms - 未記録
    legs 1 休め
    abs - 未記録

- `balance`: 部位ごとのセット数と割合です。`low` は一番セット数が少ない部位です。

- `recovery`: 部位ごとに、最後に鍛えてから何日たったかを表示します（入力の中で一番新しい日を基準に数えます）。2日以上たっていれば `OK`、それ以外は `休め` です。記録がない部位は `未記録` です。

データが読めないときや、記録が1件もないときは、エラーを出して終わります。
## テスト

    $ bash test.bash

## ライセンス

MIT License