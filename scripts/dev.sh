#!/usr/bin/env bash

set - e

rm output/images/*

python3 dev_main.py \
--config dev_config.py \
--dataset img \
--num_processes 4 \
--log_period 100