# MuscleGuard

筋トレ記録から、部位ごとのバランスと回復日数を出すコマンドです。

## 使い方

    $ cat examples/workouts.jsonl | muscleguard

## 入力

1行が1回のトレーニングのJSONです。

    {"date": "2026-11-20", "exercise": "bench_press", "muscles": {"chest": 1.0, "shoulders": 0.3, "arms": 0.3}, "sets": 3}

- `date`: トレーニングした日
- `exercise`: 種目名（メモ用で、集計には使いません）
- `muscles`: 使った部位と、その割合（メインは1.0）
- `sets`: セット数

## 出力

    balance
    chest 7.0 36.8
    back 3.0 15.8
    shoulders 2.1 11.1
    arms 3.0 15.8
    legs 3.0 15.8
    abs 0.9 4.7
    low abs
    recovery
    chest 0 休め
    back 2 OK
    shoulders 0 休め
    arms 0 休め
    legs 1 休め
    abs 1 休め

- `balance`: 部位ごとのセット数と割合です。セット数は「セット数 × 部位の割合」を合計したものです。`low` は一番セット数が少ない部位です。
- `recovery`: 部位ごとに、最後に鍛えてから何日たったかを表示します。2日以上たっていれば `OK`、それ以外は `休め` です。記録がない部位は `未記録` です。

データが読めないときや、記録が1件もないときは、エラーを出して終わります。

## インストール

    $ pip install -e ".[dev]"

## テスト

    $ python -m pytest tests -v

## ライセンス

MIT License