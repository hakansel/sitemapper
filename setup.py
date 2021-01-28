import sys

from setuptools import setup, find_packages

if sys.version_info < (3, 9):
    sys.exit('Sorry, Python < 3.9 is not supported')

setup(
    name='sitemapper',
    version='1.0.0',
    description='Yet another sitemapper',
    packages=find_packages(),
    include_package_data=True,
    author='hakansel'
)
