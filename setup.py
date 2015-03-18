from stash import __version__

from setuptools import setup, find_packages

setup(
    name='stash',
    version=__version__,
    license='MIT',
    url='https://github.com/fuzeman/stash',

    author='Dean Gardiner',
    author_email='me@dgardiner.net',

    description='Dictionary-style storage interface with a modular interface for algorithms, archives, caches and serializers',
    packages=find_packages(exclude=[
        'examples',
        'tests'
    ]),
    platforms='any',

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python'
    ],
)
