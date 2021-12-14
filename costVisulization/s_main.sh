#!/bin/bash

INITIAL_WORKING_DIRECTORY=$(pwd)

cd $INITIAL_WORKING_DIRECTORY
rm -r data;
rm -r global;
rm -r region_stats;
rm -r graphs;

mkdir -p data;
mkdir -p graphs;
mkdir -p global;
mkdir -p region_stats;

# chmod +x -r ./scripts
./scripts/ec2Info.sh
python3 scripts/jsonToCsv.py
python3 scripts/analysis.py 