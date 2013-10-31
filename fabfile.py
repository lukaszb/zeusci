from fabric.api import cd
from fabric.api import env
from fabric.api import local
from fabric.context_managers import shell_env
import os
import sys
import jinja2


def _(text):
    template = jinja2.Template(text)
    frame = sys._getframe(1)
    global_vars = frame.f_globals
    local_vars = frame.f_locals
    context = dict(global_vars, **local_vars)
    return template.render(context)


abspath = lambda *p: os.path.abspath(os.path.join(*p))

ROOT_DIR = os.path.dirname(__file__)
PROJECT_DIR = abspath(ROOT_DIR, 'exampleci')
DEVENV_DIR = abspath(ROOT_DIR, '.devenv')
PYTHON_BIN = abspath(DEVENV_DIR, 'bin', 'python')
PYTHON_VER = 'python3.3'
APP_DIR = abspath(PROJECT_DIR, 'app')
MANAGE_BIN = _('{{ PYTHON_BIN }} ' + abspath(APP_DIR, 'manage.py'))
PIP_BIN = abspath(DEVENV_DIR, 'bin', 'pip')
CONFIG_DIR = abspath(PROJECT_DIR, 'config')
REQUIREMENTS_TXT = abspath(CONFIG_DIR, 'requirements.txt')
KARMA_CONFIG = abspath(CONFIG_DIR, 'karma.conf.js')
SETUP_PY = abspath(ROOT_DIR, 'setup.py')


def _warn(msg):
    print("[WARNING] %s" % msg)


def setup_env():
    with cd(ROOT_DIR):
        if os.path.exists(DEVENV_DIR):
            _warn(_("Development environment seems to exists at {{ DEVENV_DIR }}"))
        else:
            local(_('virtualenv -p {{ PYTHON_VER }} {{ DEVENV_DIR }}'))
        local(_('{{ PIP_BIN }} install -r {{ REQUIREMENTS_TXT }}'))
        local(_('{{ PYTHON_BIN }} {{ SETUP_PY }} develop'))

def clear_env():
    with cd(ROOT_DIR):
        local(_('rm -Rf {{ DEVENV_DIR }}'))

def test_py(test_arg=None):
    watch = False
    if test_arg is None:
        test_arg = 'zeusci.zeus'
        watch = True

    with shell_env(TESTING="Yes"):
        env.ok_ret_codes = [0, 1] # in case of errors, tests should still run
        test_cmd = _('{{ MANAGE_BIN }} test {{ test_arg }}')
        print repr(test_cmd)
        cmd = _('watchmedo shell-command -w -R -p "*.py" -c "clear && {{ test_cmd }}"')
        with cd(PROJECT_DIR):
            local(test_cmd)
            if watch:
                local(cmd)

def shell():
    local(_('{{ MANAGE_BIN }} shell_plus'))

def server():
    local(_('{{ MANAGE_BIN }} runserver'))

def celery():
    local(_('{{ MANAGE_BIN }} celery worker'))

def reset_env():
    local(_('{{ MANAGE_BIN }} zeusci_reset_env'))

