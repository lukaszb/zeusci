from setuptools import setup
#from setuptools import find_packages
from setuptools.command.test import test as TestCommand

class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True
    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import pytest
        pytest.main(self.test_args)

setup(
    name="zeus-ci",
    version="0.8.0",
    description=("zeus-ci is Django based continous integration server"),
    author="Lukasz Balcerzak",
    author_email="lukaszbalcerzak@gmail.com",
    license="MIT",
    url="https://github.com/lukaszb/zeus-ci/",
    #install_requires=("gevent-websocket",),
    #setup_requires=('Django'),
    cmdclass = {'test': PyTest},
    #tests_require=['pytest', 'mock'],
    #packages=find_packages(exclude=["examples", "tests"]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Intended Audience :: Developers",
    ],
    #entry_points="""

    #[paste.server_runner]
    #paster = socketio.server:serve_paste

    #""",
)

