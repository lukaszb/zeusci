from fabric.api import cd
from fabric.api import env
from fabric.api import local
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
PROJECT_DIR = abspath(ROOT_DIR, 'zeusci')
DEVENV_DIR = abspath(ROOT_DIR, '.devenv')
PYTHON_BIN = abspath(DEVENV_DIR, 'bin', 'python')
PYTHON_VER = 'python2.7'
MANAGE_BIN = _('{{ PYTHON_BIN }} ' + abspath(PROJECT_DIR, 'manage.py'))
PIP_BIN = abspath(DEVENV_DIR, 'bin', 'pip')
CONFIG_DIR = abspath(ROOT_DIR, 'config')
REQUIREMENTS_TXT = abspath(CONFIG_DIR, 'requirements.txt')
KARMA_CONFIG = abspath(CONFIG_DIR, 'karma.conf.js')


def _warn(msg):
    print("[WARNING] %s" % msg)


def setup_env():
    with cd(ROOT_DIR):
        if os.path.exists(DEVENV_DIR):
            _warn(_("Development environment seems to exists at {{ DEVENV_DIR }}"))
        else:
            local(_('virtualenv -p {{ PYTHON_VER }} {{ DEVENV_DIR }}'))
        local(_('{{ PIP_BIN }} install -r {{ REQUIREMENTS_TXT }}'))

def clear_env():
    with cd(ROOT_DIR):
        local(_('rm -Rf {{ DEVENV_DIR }}'))

def test_py():
    env.ok_ret_codes = [0, 1] # in case of errors, tests should still run
    test_cmd = _('{{ MANAGE_BIN }} test zeus')
    print repr(test_cmd)
    cmd = _('watchmedo shell-command -w -R -p "*.py" -c "clear && {{ test_cmd }}"')
    with cd(PROJECT_DIR):
        local(test_cmd)
        local(cmd)

def test_js():
    test_cmd = 'karma start {/config/karma.conf.js'
    test_cmd = _('karma start {{ KARMA_CONFIG }}')
    local(test_cmd)

def shell():
    local(_('{{ MANAGE_BIN }} shell_plus'))

def server():
    local(_('{{ MANAGE_BIN }} runserver'))

def celery():
    local(_('{{ MANAGE_BIN }} celery worker'))

