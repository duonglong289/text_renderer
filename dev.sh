#!/usr/bin/env bash

set - e

rm output/images/*

python3 main.py \
--config config.py \
--dataset img \
--num_processes 0 \
--log_period 100