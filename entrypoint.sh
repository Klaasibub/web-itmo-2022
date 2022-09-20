#!/bin/bash
set -x
set -e

gunicorn -c ./src/config.py src.main:app --chdir src
