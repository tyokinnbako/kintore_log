# Copyright (c) 2026 Akira Niitsuma
# SPDX-License-Identifier: MIT
"""muscleguard のテスト。"""

from muscleguard import analyze


def example_workouts():
    return [
        {"date": "2026-11-20", "exercise": "bench_press", "muscles": {"chest": 1.0, "shoulders": 0.3, "arms": 0.3}, "sets": 3},
        {"date": "2026-11-21", "exercise": "lat_pulldown", "muscles": {"back": 1.0, "arms": 0.3}, "sets": 3},
        {"date": "2026-11-22", "exercise": "squat", "muscles": {"legs": 1.0, "abs": 0.3}, "sets": 3},
        {"date": "2026-11-23", "exercise": "bench_press", "muscles": {"chest": 1.0, "shoulders": 0.3, "arms": 0.3}, "sets": 4},
    ]


def test_balance():
    lines = analyze(example_workouts())
    assert "chest 7.0 36.8" in lines
    assert "back 3.0 15.8" in lines
    assert "low abs" in lines


def test_recovery():
    lines = analyze(example_workouts())
    assert "chest 0 休め" in lines
    assert "back 2 OK" in lines
    assert "legs 1 休め" in lines


def test_no_record():
    workouts = [
        {"date": "2026-11-20", "exercise": "bench_press", "muscles": {"chest": 1.0}, "sets": 3},
    ]
    lines = analyze(workouts)
    assert "back - 未記録" in lines
    assert "chest 0 休め" in lines