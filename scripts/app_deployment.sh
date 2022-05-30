#! /bin/bash
export BUNDLE_DIR_NAME="deployment"
export PROJECT_NAME="tvratings"

#exits program immediately if a command is not sucessful
set -e

source avenv/bin/activate

python -m unittest

# --junk-paths __pycache__
zip "${PROJECT_NAME}_deployment_package.zip"  externals/tvratings_skill.py -r tvratings  \
    -x *__pycache__* --quiet 
