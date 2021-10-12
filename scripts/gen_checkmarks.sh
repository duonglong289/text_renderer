#!/usr/bin/env bash

set - e

rm -r output_checkmarks
mkdir output_checkmarks

python3 custom_main.py \
--config checkmarks_config.py \
--dataset img \
--num_processes 0 \
--log_period 100