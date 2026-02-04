from setuptools import setup, find_packages

setup(
    name="foodmetrics",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pandas>=1.3.0",
        "requests>=2.25.0",
    ],
    python_requires=">=3.8",
)