#!/bin/bash
set -x
set -e

echo "Migrate..."
aerich upgrade

echo "Server is running!"
gunicorn -c ./src/config.py src.main:app --chdir src
