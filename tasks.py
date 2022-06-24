from invoke import task
from os import getcwd


@task
def lint(c):
    print("Running linting...")
    c.run("flake8 --statistics .")


@task
def format(c):
    print("Running formatting...")
    c.run("black .")


@task
def test(c):
    print("Running test...")
    pwd = getcwd()
    c.run(
        f"DATABASE_URL=sqlite://{pwd}/test.db"
        " PYTHONPATH=app"
        " pytest . --junitxml=test_results.xml --cov"
    )


@task
def db_upgrade(c):
    print("Running DB upgrade...")
    c.run("PYTHONPATH=app FLASK_APP=main flask db upgrade")


@task
def start(c):
    print("Running start...")
    c.run(
        "OAUTHLIB_INSECURE_TRANSPORT=true"
        " FLASK_DEBUG=1"
        " PYTHONPATH=app"
        " FLASK_ENV=development"
        " flask run"
    )


@task(lint, test)
def ci(c):
    print("Running CI...")
