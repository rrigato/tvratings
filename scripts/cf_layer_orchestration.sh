aws s3api put-object --bucket lambda-deployment-bundles \
    --key layers/ask_sdk_core_most_recent.zip \
    --body layers/ask_sdk_core_1_19_0.zip


aws cloudformation create-change-set \
    --stack-name alexa-skills-kit-sdk-python-layer \
    --change-set-name tvratings-new-layer-version \
    --template-body file://templates/ask_lambda_layer.template 

aws cloudformation execute-change-set \
    --stack-name alexa-skills-kit-sdk-python-layer \
    --change-set-name tvratings-new-layer-version 
