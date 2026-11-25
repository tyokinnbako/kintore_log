#!/bin/bash
# Copyright (c) 2026 Akira Niitsuma
# SPDX-License-Identifier: MIT

out=$(./kintore_log < examples/workouts.txt)

echo "$out" | grep -q "chest 7.0 53.8" || exit 1
echo "$out" | grep -q "low shoulders" || exit 1
echo "$out" | grep -q "back 2 OK" || exit 1

./kintore_log < /dev/null 2> /dev/null
if [ $? -eq 0 ]; then
    exit 1
fi