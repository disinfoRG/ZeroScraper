import os


class Cleanup:
    def __init__(self, runner):
        self.runner = runner

    def terminate(self):
        self.runner.stop()


class ProcessError(Exception):
    pass


class PIDLock:
    def __init__(self, queries, proc_name):
        self.queries = queries
        self.key = f"{proc_name}:pid"

    def __enter__(self):
        with self.queries.transaction():
            lock = self.queries.get_variable(key=self.key)
            if lock is not None and lock["value"]:
                raise ProcessError("Another discover process already running.")
            self.queries.set_variable(key=self.key, value=str(os.getpid()))

    def __exit__(self, type_, value, traceback):
        self.queries.delete_variable(key=self.key)


def pid_lock(queries, proc_name):
    return PIDLock(queries, proc_name)
