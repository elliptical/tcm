"""Setup script.

Run "python setup.py install" to install the tcm package.
"""


import os
import re
import sys

from setuptools import setup


PACKAGE_NAME = 'tcm'


if sys.version_info < (3, 4):
    raise RuntimeError('ERROR: {} requires Python 3.4 or higher'.format(PACKAGE_NAME))


def get_readme():
    """Return the contents of the package's README.rst file."""
    with open('README.rst') as readme_file:
        text = readme_file.read()
    return text


def get_version():
    """Return the version string from the package's __init__.py file."""
    with open(os.path.join(PACKAGE_NAME, '__init__.py')) as version_file:
        version_source = version_file.read()
    version_match = re.search(r"^__version__ = '([^']*)'", version_source, re.MULTILINE)
    if not version_match:
        raise RuntimeError('Could not find the version string.')
    return version_match.group(1)


setup(
    name=PACKAGE_NAME,
    author='Andrei Boulgakov',
    author_email='andrei.boulgakov@outlook.com',
    url='https://github.com/elliptical/tcm',
    license='MIT',
    platforms='All',
    description='Metaclass based runtime generator of the test methods',
    long_description=get_readme(),
    version=get_version(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Software Development :: Testing',
    ],
    keywords=[
        'python',
        'python3',
        'unittest',
        'metaclass',
    ],
    python_requires='>=3.4',
    packages=[PACKAGE_NAME],
    zip_safe=True,
)
