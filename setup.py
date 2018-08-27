"""
Setup.py for piframe
"""

import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, "piframe", "version.txt")) as f:
    version = f.read()

setup(
    name="piframe",
    version=version,
    description="A photo-frame app for the Raspbery PI",
    url="https://github.com/jmh045000/piframe",
    author="James Hall",
    author_email="james.m.f.hall@gmail.com",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    packages=find_packages("piframe"),
    install_requires=["pyyaml"],
    package_data={"piframe": ["config"]},
    entry_points={"console_scripts": ["piframe=piframe.main:main"]},
)
