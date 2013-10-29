from zeusci.zeus.conf import settings


def execute_command(cmd):
    backend = settings.COMMAND_EXECUTION_BACKEND
    return backend(cmd, timeout=settings.COMMAND_TIMEOUT)

