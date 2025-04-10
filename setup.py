from setuptools import setup, find_packages

setup(
    name="lifestory",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "streamlit",
        "flask",
        "requests",
        "python-dotenv",
    ],
) 