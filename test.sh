#!/usr/bin/env bash

mkdir -p out
for file in tests/original_tests/input_*; do
    test_number=$(echo $file | sed 's/^.*input_T\([0-9]*\)$/\1/')
    echo -n "Test $test_number started..."
    elapsed=$( { /usr/bin/env time -f "%E" /usr/bin/env python3 takuzu.py < tests/original_tests/input_T$test_number > out/myout_T$test_number; } 2>&1 )
    /usr/bin/env diff tests/original_tests/output_T$test_number out/myout_T$test_number
    echo " finished in $elapsed"
done