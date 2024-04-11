from setuptools import setup, find_packages


setup(
    name='browser',
    version='0.0.1',
    description='An OOP wrapper extension for the Python Selenium library to better manage browser actions.',
    author='Zack Plauché',
    packages=find_packages(),
    install_requires=[
        'selenium',
        'beautifulsoup4',
        'requests',
    ],
)