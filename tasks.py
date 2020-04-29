from dotenv import load_dotenv

load_dotenv()
import os
from invoke import task
from sys import platform


@task
def check(c):
    c.run("mypy .")


@task
def test(c):
    c.run("python -m unittest")


@task
def migrate(c):
    c.run("alembic upgrade head")


@task
def m2sh(c):
    c.run(os.getenv("M2_SHELL"), pty=True)


@task
def m2(c):
    c.run(f"python -m webbrowser -t '{os.getenv('M2_URL')}'")


@task
def tunnel(c):
    c.run(os.getenv("M2_TUNNEL"))
