from setuptools import setup, find_packages

with open('requirements.txt') as file:
    requirements = file.read().splitlines()

setup(
    name='wyzantapi',
    version='0.2.8',
    url='https://github.com/ZackPlauche/wyzantapi',
    author='Zack Plauche',
    author_email='zackknowspython@gmail.com',
    description='A Python Selenium API for Wyzant.com. Interact with the Wyzant website programmatically and scrape data.',
    packages=find_packages(),
    install_requires=requirements,
)