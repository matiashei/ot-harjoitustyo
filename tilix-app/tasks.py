from invoke import task

@task(name="start")
def start(ctx):
    ctx.run("python3 -m src.index", pty=True)

@task(name="test")
def test(ctx):
    ctx.run("pytest", pty=True)

@task(name="coverage-report")
def coverage_report(ctx):
    ctx.run("coverage run -m pytest", pty=True)
    ctx.run("coverage report -m", pty=True)
    ctx.run("coverage html", pty=True)

@task(name="lint")
def lint(ctx):
    ctx.run("pylint src", pty=True)

@task(name="build")
def build(ctx):
    ctx.run("python3 src/build.py", pty=True)

@task(name="format")
def format(ctx):
    ctx.run("autopep8 --in-place --recursive src", pty=True)