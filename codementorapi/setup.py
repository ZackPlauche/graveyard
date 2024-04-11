from setuptools import setup, find_packages

with open('requirements.txt') as file:
    requirements = file.read().splitlines()

setup(
    name='codementorapi',
    version='0.0.9',
    url='https://github.com/ZackPlauche/codementorapi',
    author='Zack Plauche',
    author_email='zackknowspython@gmail.com',
    description='A Python Selenium API for Codementor.com. Interact with the Codementor website programmatically and scrape data.',
    packages=find_packages(),
    install_requires=requirements,
)