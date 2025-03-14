#!/bin/bash

function tappd () {
    cd tappd-simulator
}

function parent () {
    cd ..
}

function tappd_simulator () {
    tappd
    ./tappd-simulator -l unix:/tmp/tappd.sock > tappd-log.txt 2>&1 &
    parent
}

if [ "$BUILD_ENV" == "local" ]; then
  echo "Running in local mode"
  tappd_simulator
fi

poetry run uvicorn main:app --host 0.0.0.0 --port 8000
