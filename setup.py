from setuptools import setup, find_packages
import os
import sys
import zeusci

readme_file = os.path.join(os.path.dirname(__file__), 'README.rst')
try:
    long_description = open(readme_file).read()
except IOError as err:
    sys.stderr.write("[ERROR] Cannot find file specified as "
        "``long_description`` (%s)\n" % readme_file)
    sys.exit(1)

setup(
    name = 'zeusci',
    version = zeusci.get_version(),
    url = 'http://github.com/lukaszb/zeusci',
    author = 'Lukasz Balcerzak',
    author_email = 'lukaszbalcerzak@gmail.com',
    download_url='https://github.com/lukaszb/zeusci/tags',
    description = zeusci.__doc__.strip(),
    long_description = long_description,
    zip_safe = False,
    packages = find_packages(),
    include_package_data = True,
    license = 'MIT',
    install_requires = [
        'click>=2.4',
    ],
    tests_require = [],
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Security',
        'Programming Language :: Python :: 3',
    ],
    entry_points={
        'console_scripts': [
            'zci = zeusci.cli:main',
        ],
    },
)

