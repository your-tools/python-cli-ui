# type: ignore
from invoke import call, task

SOURCES = "cli_ui"


@task
def black(c, check=False):
    print("Running black")
    cmd = f"black {SOURCES}"
    if check:
        cmd += " --check"
    c.run(cmd)


@task
def isort(c, check=False):
    print("Running isort")
    cmd = f"isort {SOURCES}"
    if check:
        cmd += " --check"
    c.run(cmd)


@task
def flake8(c):
    print("Running flake8")
    c.run(f"flake8 {SOURCES}")


@task
def mypy(c, machine_readable=False):
    print("Running mypy")
    cmd = "mypy"
    if machine_readable:
        cmd += " --no-pretty"
    else:
        cmd += " --color-output --pretty"
    c.run(cmd)


@task
def test(c):
    print("Running pytest")
    c.run("pytest")


@task
def sphinx(c, dev=False):
    print("Running sphinx")
    cmd = "sphinx-autobuild" if dev else "sphinx-build"
    with c.cd("docs"):
        c.run(f"{cmd} -W . _build/html")


@task(pre=[call(sphinx)])
def deploy_docs(c):
    with c.cd("docs"):
        c.run("ghp-import _build/html/ -p -n -m 'ghp-import automatic commit'")


@task(
    pre=[
        call(black, check=True),
        call(isort, check=True),
        call(flake8),
        call(mypy),
    ]
)
def lint(c):
    pass


@task(
    pre=[
        call(sphinx)
        ]


@task
def safety_check(c):
    c.run("safety check")
