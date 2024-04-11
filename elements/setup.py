from setuptools import setup, find_packages

with open('requirements.txt') as requirements_file:
    requirements = requirements_file.read().splitlines()

setup(
    name='elements',
    version='0.1.4',
    url='https://github.com/ZackPlauche/elements',
    author='Zack Plauche',
    author_email='zackknowspython@gmail.com',
    description='An OOP Python Selenium WebElement wrapper for with convenience methods and a structure for easier working with elements on a page.',
    packages=find_packages(),
    install_requires=requirements,
)
