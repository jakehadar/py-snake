import io

from pkg_resources import resource_string
from setuptools import setup, find_packages

VERSION = '0.0.2'


setup(
    name='py-snake',
    version=VERSION,
    author='Jake Hadar',
    author_email='jakehadar.dev@gmail.com',
    description='CLI Snake game.',
    url='https://github.com/jakehadar/py-snake',
    python_requires='>=2.7',
    include_package_data=True,
    long_description=resource_string(__name__, 'README.md').decode('utf-8'),
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
    install_requires=resource_string(__name__, 'requirements.txt').decode('utf-8'),
    license=resource_string(__name__, 'LICENSE.txt').decode('utf-8'),
    tests_require=['pytest'],
    entry_points={
        'console_scripts': ['snake=snake.run:main']
    }
)
