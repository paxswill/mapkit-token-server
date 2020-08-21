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


setup(
    name="mapkit-token-server",
    version=version,
    description="Simple MapKit JS token server",
    author="Will Ross",
    author_email="paxswill@paxswill.com",
    license="BSD",
    url="https://github.com/paxswill/mapkit-token-server",
    packages=find_packages(),
    install_requires=[
        "aiohttp == 3.5.4",
        "python-jose == 3.0.1",
        "ecdsa == 0.13",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
    ],
    python_requires=">=3.7",
)
