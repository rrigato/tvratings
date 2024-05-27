set -e


export BUCKET_NAME="${PROJECT_NAME}-app-artifacts"
export DEPLOYMENT_PACKAGE="${PROJECT_NAME}_deployment_package.zip"
export FUNCTION_NAME="${PROJECT_NAME}-alexa-skill"




python -m venv avenv

source avenv/bin/activate
pip install -r requirements/requirements-dev.txt

secret_scan_results=$(detect-secrets scan | \
python -c "import sys, json; print(json.load(sys.stdin)['results'])" )

# static scan for security credentials that terminates if any secrets are found
if [ "${secret_scan_results}" != "{}" ]; then
    echo "detect-secrets scan failed"
    exit 125
fi


python -m unittest

deactivate

echo "--------beginning bundle--------"

# removes the deployment .zip package locally if it exists
if [ -e $DEPLOYMENT_PACKAGE ]; then
    rm $DEPLOYMENT_PACKAGE
fi

zip $DEPLOYMENT_PACKAGE -r tvratings externals  \
    -x *__pycache__*  --quiet


#add tvratings_skill.py to root of project
zip -u $DEPLOYMENT_PACKAGE -j handlers/tvratings_skill.py  \
    -x *__pycache__* --quiet

echo "--------bundle complete--------"

echo $BUCKET_NAME
echo $DEPLOYMENT_PACKAGE
aws s3api put-object --bucket $BUCKET_NAME \
    --key $DEPLOYMENT_PACKAGE \
    --body $DEPLOYMENT_PACKAGE \
    --tagging "cloudformation_managed=no&project=${PROJECT_NAME}&prod=yes"


aws lambda update-function-code --function-name $FUNCTION_NAME \
    --s3-bucket $BUCKET_NAME \
    --s3-key $DEPLOYMENT_PACKAGE \
    --no-cli-pager



echo "----------------------"
echo "deployment successful"