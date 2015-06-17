from stash import __version__

from setuptools import setup, find_packages

setup(
    name='stash.py',
    version=__version__,
    license='MIT',
    url='https://github.com/fuzeman/stash.py',

    author='Dean Gardiner',
    author_email='me@dgardiner.net',

    description='Dictionary-style storage interface with a modular interface for algorithms, archives, caches and serializers',
    packages=find_packages(exclude=[
        'examples',

        'tests',
        'tests.*'
    ]),
    platforms='any',

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Database :: Front-Ends'
    ],
)
