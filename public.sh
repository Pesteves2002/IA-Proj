#!/usr/bin/env bash

mkdir -p outTest
for file in tests/custom_tests/ct*; do
    test_number=$(echo $file | sed 's/^.*ct\([0-9]*\)$/\1/')
    echo -n "Test $test_number started..."
    elapsed=$( { /usr/bin/env time -f "%E" /usr/bin/env python3 takuzu.py < tests/custom_tests/ct$test_number > outTest/ct$test_number; } 2>&1 )
    /usr/bin/env diff tests/custom_tests/ct$test_number outTest/ct$test_number
    echo " finished in $elapsed"
done