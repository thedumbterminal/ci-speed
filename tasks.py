from invoke import task


@task
def lint(c):
    print("Running linting...")
    c.run("flake8 --statistics .")


@task
def format(c):
    print("Running formatting...")
    c.run("black .")


@task(lint)
def ci(c):
    print("Running CI...")
