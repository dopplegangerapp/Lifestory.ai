from setuptools import setup, find_packages

setup(
    name="lifestoryai",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        'flask',
        'flask-sqlalchemy',
        'pytest',
    ],
) 