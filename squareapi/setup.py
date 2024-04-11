from setuptools import setup, find_packages

with open('requirements.txt') as file:
    requirements = file.read().splitlines()

setup(
    name='squareapi',
    version='0.0.2',
    description='Square API',
    author='Zack Plauché',
    packages=find_packages(),
    install_requires=requirements,
)