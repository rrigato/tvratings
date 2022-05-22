aws cloudformation create-stack --stack-name tvratings-alexa-skill \
--template-body file://templates/tvratings_alexa_skill.template \
--tags Key=project,Value=tvratings Key=prod,Value=yes Key=multi_repo,Value=yes

