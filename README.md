# alexa-skill-link
https://www.amazon.com/dp/B0B5596H7C/

Enabling the above skill allows you to get the television ratings for Adult Swim's Saturday night
Toonami television block.

# getting-started

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


# detect-secrets
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

# feature-requests
- Get the highest and lowest ratings for a provided television show name
- Get the first and last showing of a show
- Highest and lowest ratings for a time period 