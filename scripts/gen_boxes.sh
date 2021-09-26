#!/usr/bin/env bash

set - e

rm output_boxes/images/*
mkdir output_boxes

python3 custom_main.py \
--config boxes_config.py \
--dataset img \
--num_processes 0 \
--log_period 100