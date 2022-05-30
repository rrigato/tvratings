#! /bin/bash
export BUNDLE_DIR_NAME="deployment"
export PROJECT_NAME="tvratings"
# export PYTHONPYCACHEPREFIX="~/Documents/project_pycache"

#exits program immediately if a command is not sucessful
set -e

source avenv/bin/activate

python -m unittest
