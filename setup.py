"""
Most simple barebones setup.py
"""

from setuptools import setup, find_packages

setup(
    name="test-package",
    version="1.0",
    packages=find_packages(where="package"),
)
