from fabric.api import cd
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
DEVENV_DIR = abspath(ROOT_DIR, 'devenv')
MANAGE_BIN = abspath(PROJECT_DIR, 'manage.py')
PYTHON_BIN = abspath(DEVENV_DIR, 'bin', 'python')
CONFIG_DIR = abspath(ROOT_DIR, 'config')
KARMA_CONFIG = abspath(CONFIG_DIR, 'karma.conf.js')


def _error(msg, code=1):
    print("ERROR: %s" % msg)
    sys.exit(code)


def setup_env():
    if os.path.exists(DEVENV_DIR):
        _error(_("Development environment seems to exists at {{ DEVENV_DIR }}"))
    with cd(ROOT_DIR):
        local('tox -e devenv')

def test_py():
    test_cmd = _('{{ PYTHON_BIN }} {{ MANAGE_BIN }} test zeus')
    cmd = _('watchmedo shell-command -w -R -p "*.py" -c "clear && {{ test_cmd }}"')
    with cd(PROJECT_DIR):
        local(test_cmd)
        local(cmd)

def test_js():
    test_cmd = 'karma start {/config/karma.conf.js'
    test_cmd = _('karma start {{ KARMA_CONFIG }}')
    local(test_cmd)

