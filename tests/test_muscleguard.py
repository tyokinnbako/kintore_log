# Copyright (c) 2026 Akira Niitsuma
# SPDX-License-Identifier: MIT
"""muscleguard のテスト。"""

import io
import subprocess
from datetime import date

import pytest

from muscleguard import InputError, compute_balance, compute_recovery, parse_feeling, parse_workout, parse_workouts, score_to_status

REF_DATE = date(2026, 11, 24)


def make_workout(when="2026-11-20", muscles=None, sets=3):
    if muscles is None:
        muscles = {"chest": 1.0}
    return parse_workout(
        {"date": when, "exercise": "bench_press", "muscles": muscles, "weight": 60, "reps": 10, "sets": sets},
        1,
    )


def make_feeling(muscle="chest", soreness=1, fatigue=1, condition=5, pain=False):
    return parse_feeling(
        {"date": "2026-11-24", "muscle": muscle, "soreness": soreness, "fatigue": fatigue, "condition": condition, "pain": pain},
        1,
    )


def example_workouts():
    return [
        make_workout("2026-11-20", {"chest": 1.0, "shoulders": 0.3, "arms": 0.3}, 3),
        make_workout("2026-11-21", {"back": 1.0, "arms": 0.3}, 3),
        make_workout("2026-11-22", {"legs": 1.0, "abs": 0.3}, 3),
        make_workout("2026-11-23", {"chest": 1.0, "shoulders": 0.3, "arms": 0.3}, 4),
    ]


WORKOUTS_JSONL = """{"date": "2026-11-20", "exercise": "bench_press", "muscles": {"chest": 1.0, "shoulders": 0.3, "arms": 0.3}, "weight": 60, "reps": 10, "sets": 3}
{"date": "2026-11-21", "exercise": "lat_pulldown", "muscles": {"back": 1.0, "arms": 0.3}, "weight": 45, "reps": 10, "sets": 3}
{"date": "2026-11-22", "exercise": "squat", "muscles": {"legs": 1.0, "abs": 0.3}, "weight": 70, "reps": 10, "sets": 3}
{"date": "2026-11-23", "exercise": "bench_press", "muscles": {"chest": 1.0, "shoulders": 0.3, "arms": 0.3}, "weight": 65, "reps": 8, "sets": 4}
"""


def test_parse_workout_valid():
    workout = make_workout()
    assert workout["exercise"] == "bench_press"
    assert workout["sets"] == 3
    assert workout["weight"] == 60.0


def test_parse_workout_unknown_muscle():
    with pytest.raises(InputError):
        parse_workout(
            {"date": "2026-11-20", "exercise": "bench_press", "muscles": {"neck": 1.0}, "weight": 60, "reps": 10, "sets": 3},
            1,
        )


def test_parse_workout_negative_weight():
    with pytest.raises(InputError):
        parse_workout(
            {"date": "2026-11-20", "exercise": "bench_press", "muscles": {"chest": 1.0}, "weight": -1, "reps": 10, "sets": 3},
            1,
        )


def test_parse_feeling_pain_must_be_bool():
    with pytest.raises(InputError):
        parse_feeling(
            {"date": "2026-11-24", "muscle": "chest", "soreness": 1, "fatigue": 1, "condition": 5, "pain": "yes"},
            1,
        )


def test_parse_workouts_bad_json():
    with pytest.raises(InputError):
        parse_workouts(io.StringIO("{not json}\n"))


def test_score_to_status_boundaries():
    assert score_to_status(80) == "良好"
    assert score_to_status(79) == "やや注意"
    assert score_to_status(40) == "注意"
    assert score_to_status(39) == "休養を優先"


def test_recovery_soreness_5_forces_rest():
    workouts = [make_workout("2026-11-23")]
    feelings = [make_feeling(soreness=5, fatigue=0)]
    result = compute_recovery(workouts, feelings, REF_DATE)
    assert result["chest"]["status"] == "休養を優先"


def test_recovery_pain_forces_rest():
    workouts = [make_workout("2026-11-23")]
    feelings = [make_feeling(pain=True)]
    result = compute_recovery(workouts, feelings, REF_DATE)
    assert result["chest"]["status"] == "休養を優先"


def test_recovery_no_feeling_is_pending():
    workouts = [make_workout("2026-11-23")]
    result = compute_recovery(workouts, [], REF_DATE)
    assert result["chest"]["score"] is None
    assert result["chest"]["status"] == "判定保留"


def test_recovery_no_workout_is_no_record():
    result = compute_recovery([], [], REF_DATE)
    assert result["chest"]["score"] is None
    assert result["chest"]["status"] == "未記録"


def test_balance_low():
    balance = compute_balance(example_workouts(), 7, REF_DATE)
    assert balance["sufficient_data"] is True
    assert balance["low"] == ["abs"]
    assert balance["sets"]["chest"] == 7.0


def test_balance_insufficient_data():
    balance = compute_balance([make_workout()], 7, REF_DATE)
    assert balance["sufficient_data"] is False
    assert balance["low"] == []


def test_cli_balance_stdout():
    result = subprocess.run(["muscleguard", "balance"], input=WORKOUTS_JSONL, text=True, capture_output=True)
    assert result.returncode == 0
    assert "chest 7.0 36.8" in result.stdout
    assert "low abs" in result.stdout
    assert result.stderr == ""


def test_cli_invalid_input_exit_2():
    result = subprocess.run(["muscleguard", "balance"], input="{not json}\n", text=True, capture_output=True)
    assert result.returncode == 2
    assert result.stdout == ""
    assert "エラー" in result.stderr