# CI Speed

[![Python application](https://github.com/thedumbterminal/ci-speed/actions/workflows/python-app.yml/badge.svg)](https://github.com/thedumbterminal/ci-speed/actions/workflows/python-app.yml)

Historcally analyse CI builds for test duration, failures and more.

For the UI please see:

https://github.com/thedumbterminal/ci-speed-ui

## Demo

Video introduction:

https://youtu.be/trr3Rv3VhQk

Live site:

https://ci-speed.herokuapp.com

## Requirements

* Heroku CLI https://devcenter.heroku.com/articles/heroku-cli
* pyenv https://github.com/pyenv/pyenv#simple-python-version-management-pyenv
* Docker https://www.docker.com/get-started/

## Install

### Server

```
scripts/setup_pyenv.sh
scripts/install.sh
```

### Database

```
docker run --name postgresql -e POSTGRES_USER=myusername -e POSTGRES_PASSWORD=mypassword -p 5432:5432 -v ${PWD}/data:/var/lib/postgresql/data -d postgres
docker ps -a
```

To access use:

```
psql -h 127.0.0.1 -U myusername myusername
```

## Run

```
invoke start
```

Dev server is available at:

http://127.0.0.1:5000


Or with github auth:

```
GITHUB_OAUTH_CLIENT_ID=xxx GITHUB_OAUTH_CLIENT_SECRET=xxx SQLALCHEMY_ECHO=1 invoke start
```

### Production mode

```
honcho start
```

## Example actions

Upload test run:

```
curl -F 'file=@samples/junit_perl.xml' http://localhost:5000/test_runs/
```

## Deploy

Once code has been merged to the `main` branch, you can deploy from your local machine, using:

```
invoke deploy
```

Once deployed the API will visible at the following URL:

https://ci-speed.herokuapp.com

## Utilities

### Listing routes

```
PYTHONPATH=app flask routes
```

### Clearing the database

```
PYTHONPATH=app flask cleardb
PYTHONPATH=app FLASK_APP=main flask db stamp 'base'
PYTHONPATH=app FLASK_APP=main flask db upgrade
```

### Database migrations

To create a new migration:

```
PYTHONPATH=app FLASK_APP=main flask db revision -m "Some comment here"
```

To update your local DB to the latest version run:

```
invoke db-upgrade
```

To update the production DB to the latest version run:

```
heroku run 'PYTHONPATH=app FLASK_APP=main flask db upgrade'
```

## Environment Variables

See also the built in flask environment variables.

* DATABASE_URL - Set the PostgreSQL DSN to use other than the default.
* SERVER_URL_BASE - Set the base schema and domain when creating URLs to the UI app.
* UI_URL_BASE - Set the base schema and domain when proxying to UI assets.
* UI_URL_PATH - Set the path when proxying to UI assets.
* FLASK_SECRET_KEY - Use a random value for flask auth storage. `echo "import secrets\nprint(secrets.token_urlsafe())" | python`
* GITHUB_OAUTH_CLIENT_ID - Set to github oauth app client ID.
* GITHUB_OAUTH_CLIENT_SECRET - Set to github oauth app client secret.
* OAUTHLIB_INSECURE_TRANSPORT - Set to `true` when testing auth locally.
* SQLALCHEMY_ECHO - Log all SQL statements.

## Tech
* Python
  * Flask https://flask-restx.readthedocs.io/en/latest/
  * Marshmallow https://flask-marshmallow.readthedocs.io/en/latest/
  * SQLAlchemy
  * Alembic https://flask-migrate.readthedocs.io/en/latest/
* Postgres
* Heroku

## Todo

* Most failing tests
* Longest tests
* Flaky tests
* Marking test runs as public
* Newest / oldest tests
* Diff results from last run
* Organisation support so multiple users can share projects

### CI Integrations
* Github actions

### Client libraries

* Node.js
* Python
* Perl
