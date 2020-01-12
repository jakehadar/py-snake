import io
import os

from pkg_resources import resource_string
from setuptools import setup, find_packages

MAJOR = 0
MINOR = 0
PATCH = 2

VERSION = '{major}.{minor}.{patch}'.format(major=MAJOR, minor=MINOR, patch=PATCH)


def parse_resource_string(filename):
    text = None
    try:
        text = resource_string(__name__, filename).decode('utf-8')
    except NotImplementedError:
        # XXX: It is considered an anti-pattern to use __file__ or __path__ for locating package resource (despite its
        # popularity in the dev community) because it breaks PEP 302-based import hooks, including when importing from
        # zip files and Python Eggs. The correct pattern is to use pkg_resources.resource_string instead, however this
        # seems to be incompatible with Python3...
        here = os.path.abspath(os.path.dirname(__file__))
        text = io.open(os.path.join(here, filename), encoding='utf-8').read()
    finally:
        return text


setup(
    name='py-snake',
    version=VERSION,
    author='Jake Hadar',
    author_email='jakehadar.dev@gmail.com',
    description='CLI Snake game.',
    url='https://github.com/jakehadar/py-snake',
    python_requires='>=2.7',
    include_package_data=True,
    long_description=parse_resource_string('README.md'),
    long_description_content_type='text/markdown',
    keywords='snake game python cli command line',
    packages=find_packages(exclude=['tests', 'screenshots']),
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'Natural Language :: English',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Topic :: Games/Entertainment :: Arcade',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python',
    ],
    install_requires=parse_resource_string('requirements.txt'),
    license=parse_resource_string('LICENSE.txt'),
    tests_require=['pytest'],
    entry_points={
        'console_scripts': ['snake=snake.run:main']
    }
)
