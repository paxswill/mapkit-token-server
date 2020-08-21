#!/usr/bin/env python3
from setuptools import setup, find_packages
import re
import sys
import os.path

src_dir = "mapkit_token_server"

setup_dir = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(setup_dir, src_dir, "__init__.py"), "r") as f:
    init_contents = ""
    for line in f:
        init_contents += line + "\n"

version = re.search(
    r"""^__version__ *= *u?['"]([^'"]*)['"]""",
    init_contents,
    re.MULTILINE
)

if version:
    version = version.group(1)
else:
    raise Exception(f"Unable to find __version__ in {src_dir}/__init__.py")


with open(os.path.join(setup_dir, "requirements.txt"), "r") as f:
    requirements = list(f.readlines())


setup(
    name="mapkit-token-server",
    version=version,
    description="Simple MapKit JS token server",
    author="Will Ross",
    author_email="paxswill@paxswill.com",
    license="BSD",
    url="https://github.com/paxswill/mapkit-token-server",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
    ],
    python_requires=">=3.7",
)
