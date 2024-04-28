#!/bin/bash
echo "Starting benchmark server"
echo "HEADLESS: $HEADLESS, TEST_FILE: $TEST_FILE"
if [[ "$HEADLESS" == "true" ]]; then
    python3 /var/regex/run-benchmarks.py $TEST_FILE
else
    python3 benchmark_server/manage.py runserver 0.0.0.0:8000
fi