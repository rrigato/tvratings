#! /bin/bash

export BUNDLE_DIR_NAME="deployment"
export PROJECT_NAME="tvratings"
export DEPLOYMENT_PACKAGE="${PROJECT_NAME}_deployment_package.zip"

#exits program immediately if a command is not sucessful
set -e

source avenv/bin/activate

python -m unittest

if [ -e $DEPLOYMENT_PACKAGE ]; then
    rm $DEPLOYMENT_PACKAGE
fi

zip $DEPLOYMENT_PACKAGE -r tvratings externals  \
    -x *__pycache__*  --quiet


#add tvratings_skill.py to root of project
zip -u $DEPLOYMENT_PACKAGE -j ahandlers/tvratings_skill.py  \
    -x *__pycache__* --quiet

deactivate

echo "deployment successful"