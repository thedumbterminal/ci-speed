from invoke import task

@task
def lint(c):
    print('Running linting...')
    c.run('flake8 --statistics .')

@task(lint)
def ci(c):
    print('Running CI...')
