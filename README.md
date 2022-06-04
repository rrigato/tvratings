Amazon alexa skill for analyzing television ratings

# TODO
- update cloudformation stacks description for both stacks
- create lambda function for custom skill
- create ask skill in skills console
- repo layer implemetnation


# getting_started

1) Create a virtual environment and install dependencies:

```bash
python -m venv avenv
source avenv/bin/activate
pip install -r requirements/requirements-dev.txt
```

2) run unittests and make sure they pass

```bash
python -m unittest
```

3) install [aws cli v2](https://aws.amazon.com/cli/) for working with aws resources locally 


# deploy-application
```bash
chmod +x scripts/app_deployment.sh
scripts/app_deployment.sh
```


# detect_secrets
implement to ensure no secrets are commited locally:

setup a baseline where all tracked files will be compared to:
```bash
detect-secrets scan > .secrets.baseline
```

compare all tracked files to baseline the ```results``` key should be ```{}``` if no secrets are present
```bash
detect-secrets scan | \
python3 -c "import sys, json; print(json.load(sys.stdin)['results'])"
```
