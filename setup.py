#!/usr/bin/env python2
from setuptools import find_packages, setup


def get_version():
    with open('VERSION') as f:
        return f.read()


setup(
    name="gtfs_parser",
    version=get_version(),
    url="https://github.com/johnbrussell/gtfs_parser",
    author="John Russell",
    author_email="john.russell@tufts.edu",
    packages=find_packages(),
    include_package_data=True,
    install_requires=open("requirements.in").readlines(),
    tests_require=open("requirements.testing.in").readlines(),
    description="GTFS parser",
    long_description=open("README.md").read()
)
