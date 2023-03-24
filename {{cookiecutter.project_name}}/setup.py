from setuptools import find_packages
from setuptools import setup

setup(
    name="{{cookiecutter.project_name}}",
    packages=find_packages(),
    version="0.1.0",
    description="{{cookiecutter.project_name}}_description",
    author="{{cookiecutter.author}}",
    license="{{cookiecutter.license}}",
)
