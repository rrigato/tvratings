aws cloudformation create-stack --stack-name tvratings-alexa-skill \
--template-body file://templates/tvratings_alexa_skill.template \
--tags Key=project,Value=tvratings Key=prod,Value=yes Key=multi_repo,Value=yes

aws cloudformation update-stack --stack-name tvratings-alexa-skill \
--template-body file://templates/tvratings_alexa_skill.template \
--tags Key=project,Value=tvratings Key=prod,Value=yes Key=multi_repo,Value=yes


aws cloudformation create-stack --stack-name tvratings-alexa-skill-permissions \
--template-body file://templates/alexa_skill_permissions.template \
--parameters ParameterKey=alexaSkillId,ParameterValue=<add_alexa_skill_id> \
--tags Key=project,Value=tvratings Key=prod,Value=yes Key=multi_repo,Value=yes
