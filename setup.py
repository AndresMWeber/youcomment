from setuptools import setup, find_packages
from os import path
import io
import re

__here__ = path.abspath(path.dirname(__file__))
__project__ = 'youcomment'
__version__ = '0.0.0'
__url__ = 'https://github.com/andresmweber/%s' % __project__

with io.open(path.join(__here__, __project__, 'version.py')) as ver_file:
    mo = re.search(
        r"^__version__ = ['\"]([^'\"]*)['\"]", ver_file.read(), re.M)
    __version__ = mo.group(1)

with io.open(path.join(__here__, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

with io.open(path.join(__here__, 'CHANGELOG.md'), encoding='utf-8') as f:
    changelog = f.read()

setup(
    name=__project__,
    version=__version__,
    url=__url__,
    description='A bot for comparing top-level youtube comments and reddit comments.',
    long_description='\n\n'.join([long_description, changelog]),
    author='Andres Weber',
    author_email='andresmweber@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='reddit youtube comment top compare bot',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=['praw',
                      'google-api-python-client',
                      'google-auth',
                      'google-auth-oauthlib',
                      'google-auth-httplib2',
                      'peewee',
                      'pyyaml'],
    extras_require={
        'test': ['nose', 'coverage'],
        'dev': ['nose', 'coverage']
    },
    project_urls={
        'Bug Reports': 'https://github.com/pypa/sampleproject/issues',
        'Source': 'https://github.com/pypa/sampleproject/',
    },
    test_suite="tests",
    # package_data={
    #     'sample': ['package_data.dat'],
    # },
    # data_files=[('my_data', ['data/data_file'])],
)
