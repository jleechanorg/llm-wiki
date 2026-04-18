#!/usr/bin/env python3
"""Run SWE-bench evaluation with explicit Docker host."""
import os

# MUST set DOCKER_HOST BEFORE importing docker
os.environ['DOCKER_HOST'] = 'unix:///Users/jleechan/.docker/run/docker.sock'

import sys
sys.argv = [
    '__main__.py',
    '--dataset_name', 'princeton-nlp/SWE-bench_Lite',
    '--predictions_path', '/tmp/swebench_eval_scale/predictions.jsonl',
    '--max_workers', '4',
    '--run_id', 'autor_sr_multi_20260418',
    '--report_dir', '/tmp/swebench_eval_scale/reports',
]

from swebench.harness.run_evaluation import main

if __name__ == "__main__":
    main()