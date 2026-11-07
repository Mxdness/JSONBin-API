# JSONBin BDD API tests (behave + Allure + Jenkins)

## Project layout
```
custom_runner.py          # runs behave for a tag and writes Allure results
requirements.txt
Jenkinsfile               # parameterized pipeline (TAG = @tag1 | @tag2)
docker-compose.yaml       # Jenkins
jenkins/                  # Dockerfile, plugins.txt, casc.yaml
framework/jsonbin_client.py
features/
  api.feature
  environment.py          # failure screenshot + bin cleanup hooks
  steps/api_steps.py
```

## Run locally
```
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env          # put your real JSONBIN_MASTER_KEY in it
python custom_runner.py --tag @tag1
python custom_runner.py --tag @tag2
allure serve reports/allure-results      # optional, needs Allure CLI
```

## Jenkins
1. `cp .env.example .env` (same folder as docker-compose.yaml) and set the key.
2. `docker compose up -d --build`, open http://localhost:8080, unlock with
   `docker logs jsonbin-jenkins` (initial admin password). When asked about plugins,
   choose "Select plugins to install" -> none/minimum, the image already has what it needs.
3. Push this project to a Git repo.
4. New Item -> Pipeline -> "Pipeline script from SCM" -> Git -> your repo URL, Script Path `Jenkinsfile`.
5. Build with Parameters: run once with `@tag1`, once with `@tag2`. The "Allure Report" link
   appears on each build.

If the build says the Allure commandline "allure" is not found:
Manage Jenkins -> Tools -> Allure Commandline -> Add (name `allure`, install automatically).
If the credential is missing: Manage Jenkins -> Credentials -> add "Secret text", ID `jsonbin-master-key`.
