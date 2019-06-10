# from distutils.core import setup
from pip._internal.req import parse_requirements
from setuptools import find_packages
from setuptools import setup

setup(
    name='Python example',
    version='1.0',
    packages=['mypackage'],
    install_requires=[
        str(ir.req) for ir in parse_requirements('requirements.txt', session=False)
    ],
)
