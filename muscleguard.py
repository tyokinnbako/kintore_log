# Copyright (c) 2026 Akira Niitsuma
# SPDX-License-Identifier: MIT
"""筋トレ記録から部位バランスと回復日数を出すコマンド。"""

import json
import sys
from datetime import date

MUSCLES = ["chest", "back", "shoulders", "arms", "legs", "abs"]


def analyze(workouts):
    lines = []
    sets = {muscle: 0.0 for muscle in MUSCLES}
    for workout in workouts:
        for muscle, involvement in workout["muscles"].items():
            if muscle in sets:
                sets[muscle] += workout["sets"] * involvement
    total = sum(sets.values())
    lines.append("balance")
    for muscle in MUSCLES:
        if total > 0:
            share = sets[muscle] / total * 100
        else:
            share = 0.0
        lines.append(f"{muscle} {sets[muscle]:.1f} {share:.1f}")
    low = MUSCLES[0]
    for muscle in MUSCLES:
        if sets[muscle] < sets[low]:
            low = muscle
    lines.append("low " + low)
    today = max(workout["date"] for workout in workouts)
    lines.append("recovery")
    for muscle in MUSCLES:
        dates = [w["date"] for w in workouts if muscle in w["muscles"]]
        if not dates:
            lines.append(f"{muscle} - 未記録")
            continue
        passed = (date.fromisoformat(today) - date.fromisoformat(max(dates))).days
        if passed >= 2:
            status = "OK"
        else:
            status = "休め"
        lines.append(f"{muscle} {passed} {status}")
    return lines


def main():
    try:
        workouts = [json.loads(line) for line in sys.stdin if line.strip()]
    except json.JSONDecodeError:
        print("muscleguard: エラー JSON として読めません", file=sys.stderr)
        sys.exit(2)
    if not workouts:
        print("muscleguard: エラー 筋トレ記録がありません", file=sys.stderr)
        sys.exit(2)
    for line in analyze(workouts):
        print(line)


if __name__ == "__main__":
    main()