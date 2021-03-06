#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Note: To use the 'upload' functionality of this file, you must:
#   $ pip install twine
"""setup.py."""
import io
import os
import sys
from shutil import rmtree
from typing import Dict, List  # noqa, flake8
from git import Repo
from twine.commands.upload import main as twineupload

from setuptools import find_packages, setup, Command, sandbox

from pipenv.project import Project
from pipenv.utils import convert_deps_to_pip

pfile = Project(chdir=False).parsed_pipfile


# Package meta-data.
NAME = 'ubee_router_reset'
DESCRIPTION = 'Reset ubee router automatically by checking if internet is up then'\
    'restoring backup settings automatically using selenium.'
URL = 'https://github.com/aaronsewall/ubee_router_reset'
EMAIL = 'aaronsewall@gmail.com'
AUTHOR = 'Aaron Sewall'
REQUIRES_PYTHON = '>=3.0'
VERSION = None

# What packages are required for this module to be executed?
REQUIRED = convert_deps_to_pip(pfile['packages'], r=False)

# What packages are optional?
EXTRAS = {
    'dev': convert_deps_to_pip(pfile['dev-packages'], r=False),
}

# The rest you shouldn't have to touch too much :)
# ------------------------------------------------
# Except, perhaps the License and Trove Classifiers!
# If you do change the License, remember to change the Trove Classifier for that!

here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in file!
try:
    with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = '\n' + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

# Load the package's __version__.py module as a dictionary.
about = {}  # type: Dict[str, str]
if not VERSION:
    with open(os.path.join(here, NAME, '__version__.py')) as f:
        exec(f.read(), about)  # nosec
else:
    about['__version__'] = VERSION


class UploadCommand(Command):
    """Support setup.py upload."""

    description = 'Build and publish the package.'
    user_options = []  # type: List

    @staticmethod
    def status(s):
        """Print things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        """Not implemented."""
        pass

    def finalize_options(self):
        """Not implemented."""
        pass

    def run(self):
        """
        Remove previous builds, and build source and wheel distributions.

        Also upload to pypi and push git tags.
        """
        try:
            self.status('Removing previous builds…')
            rmtree(os.path.join(here, 'dist'))
        except OSError:
            pass

        self.status('Building Source and Wheel (universal) distribution…')
        sandbox.run_setup('setup.py', ['sdist', 'bdist_wheel', '--universal'])

        self.status('Uploading the package to PyPI via Twine…')
        twineupload("dist/*")
        self.status('Pushing git tags…')
        repo = Repo(os.getcwd())
        tag_name = 'v{0}'.format(about['__version__'])
        repo.create_tag(tag_name)
        repo.remote('origin').push(tag_name)
        sys.exit()


setup(
    name=NAME,
    version=about['__version__'],
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(exclude=('tests',)),
    # If your package is a single module, use this instead of 'packages':
    # py_modules=['mypackage'],

    # entry_points={
    #     'console_scripts': ['mycli=mymodule:cli'],
    # },
    install_requires=REQUIRED,
    extras_require=EXTRAS,
    include_package_data=True,
    license='MIT',
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
    # $ setup.py publish support.
    cmdclass={
        'upload': UploadCommand,
    },
)
