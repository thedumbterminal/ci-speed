# ci-speed
Measure CI time

## Requirements

* Heroku CLI https://devcenter.heroku.com/articles/heroku-cli
* pyenv https://github.com/pyenv/pyenv#simple-python-version-management-pyenv
* Docker https://www.docker.com/get-started/

## Install

### Server

```
scripts/install.sh
```

### Database

```
docker run --name postgresql -e POSTGRES_USER=myusername -e POSTGRES_PASSWORD=mypassword -p 5432:5432 -v ${PWD}/data:/var/lib/postgresql/data -d postgres
docker ps -a
```

## Run

```
FLASK_DEBUG=1 PYTHONPATH=app flask run
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
curl -F 'file=@samples/junit_perl.xml' http://localhost:5000/test_runs/
```

## Deploy

Once code has been merged to the `main` branch, you can deploy from your local machine, using:

```
git push heroku main:main
```

Once deployed the API will visible at the following URL:

https://ci-speed.herokuapp.com

## Database migrations

To create a new migration:

```
PYTHONPATH=app FLASK_APP=main flask db migrate -m "Some comment here"
```

To update your local DB to the latest version run:

```
PYTHONPATH=app FLASK_APP=main flask db upgrade
```

To update the production DB to the latest version run:

```
heroku run 'PYTHONPATH=app FLASK_APP=main flask db upgrade'
```

## Environment Variables

See also the built in flask environment variables.

* DATABASE_URL - Set the PostgreSQL DSN to use other than the default.
* UI_URL_BASE - Set the prefix when creating URLs to the UI app.

## Tech
* Python
  * Flask https://flask-restx.readthedocs.io/en/latest/
  * Marshmallow https://flask-marshmallow.readthedocs.io/en/latest/
  * SQLAlchemy
  * Alembic https://flask-migrate.readthedocs.io/en/latest/
* Postgres
* Heroku

## Todo

* Auth
* Viewing test results
* Most failing tests
* Longest tests
* Flaky tests
* Number of tests
* Marking test runs as public
* users -> projects -> test runs -> test suites -> test cases
* newest / oldest tests
* diff results from last run

### CI Integrations
* Github actions

### Client libraries

* Node.js
* Python
* Perl
