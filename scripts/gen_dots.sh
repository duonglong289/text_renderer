#!/usr/bin/env bash

set - e

rm output_dots -r
mkdir output_dots

python3 custom_main.py \
--config dots_config.py \
--dataset img \
--num_processes 0 \
--log_period 100