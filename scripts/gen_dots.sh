#!/usr/bin/env bash

set - e

rm output/* -r

python3 dots_main.py \
--config dots_config.py \
--dataset img \
--num_processes 0 \
--log_period 100