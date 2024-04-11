from setuptools import setup, find_packages

with open('requirements.txt') as file:
    requirements = file.read().splitlines()

setup(
    name='pages',
    version='0.2.0',
    url='https://github.com/ZackPlauche/pages',
    author='Zack Plauche',
    author_email='zackknowspython@gmail.com',
    description='A simple library for creating page objects in Python',
    packages=find_packages(),
    install_requires=requirements,
)