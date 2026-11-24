markdown
# MuscleGuard

筋トレ記録から、部位ごとのバランスと回復日数を出すコマンドです。

## 使い方

```sh
$ cat examples/workouts.jsonl | muscleguard
入力
1行が1回のトレーニングのJSONです。

json
{"date": "2026-11-20", "exercise": "bench_press", "muscles": {"chest": 1.0, "shoulders": 0.3, "arms": 0.3}, "weight": 60, "reps": 10, "sets": 3}
date: トレーニングした日
exercise: 種目名
muscles: 使った部位と、その割合（メインは1.0）
weight: 重さ（kg）
reps: 回数
sets: セット数
出力
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
balance: 部位ごとのセット数と割合です。セット数は「セット数 × 部位の割合」を合計したものです。low は一番セット数が少ない部位です。
recovery: 部位ごとに、最後に鍛えてから何日たったかを表示します。2日以上たっていれば OK、それ以外は 休め です。記録がない部位は 未記録 です。
入力がJSONとして読めないときや、記録が0件のときはエラーを出して終了します。

インストール
sh
$ pip install -e ".[dev]"
テスト
sh
$ python -m pytest tests -v
ライセンス
MIT Licenseです。詳しくは LICENSE を見てください。


**LICENSE**（新しいファイルを作って、下の内容をそのまま入れて保存する）
MIT License

Copyright (c) 2026 Akira Niitsuma

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.