$bundle_dir_name="deployment"
$project_name="tvratings"

$env:PYTHONPYCACHEPREFIX="${HOME}\\Documents\\project_pycache"


python -m unittest

(detect-secrets scan | ConvertFrom-Json).results