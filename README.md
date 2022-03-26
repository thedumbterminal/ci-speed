# ci-speed
Measure CI time

## Requirements

* Heroku CLI https://devcenter.heroku.com/articles/heroku-cli
* pyenv https://github.com/pyenv/pyenv#simple-python-version-management-pyenv

## Install

```
scripts/install.sh
```

## Run

```
python ./app/main.py
```

Dev server available at:

http://127.0.0.1:5000

### Production mode

```
honcho start
```

## Example actions

Upload test run:

```
curl -F 'file=@samples/junit_perl.xml' http://localhost:5000/test_run/
```

## Deploy

Deploys automatically to heroku on main branch merge, app available at:

https://ci-speed.herokuapp.com

## Tech
* Python
  * Flask
* Postgres
* Heroku / GCP Cloud functions?
* Single page app

## Todo

### Web UI
* Signup
* Login
* Viewing test runs
* Viewing test results
* Most failing tests
* Longest tests
* Flakey tests


### API
* Result upload
* Viewing test runs
* Viewing test results
* Most failing tests
* Longest tests
* Flakey tests


### CI Integrations
* Github actions

### Client libraries

* Node.js
* Python
* Perl
