from invoke import task

@task(name="start")
def start(ctx):
    ctx.run("python3 -m src.index")

@task(name="test")
def test(ctx):
    ctx.run("pytest")

@task(name="coverage-report")
def coverage_report(ctx):
    ctx.run("coverage run -m pytest")
    ctx.run("coverage report -m")
    ctx.run("coverage html")

@task(name="lint")
def lint(ctx):
    ctx.run("pylint src")