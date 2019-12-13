from fabric import task

middle2_host = "git@git.middle2.com"
container_name = "tainan-sun-500796"


def with_docker(cmd):
    return f"run {container_name} {cmd}"


@task(hosts=[middle2_host])
def db_current(c):
    c.run(with_docker("alembic current -v"))


@task(hosts=[middle2_host])
def db_migrate(c):
    c.run(with_docker("alembic upgrade head"))
