#!/usr/bin/env python

"""Viable Integrations for Mapbox
"""

from setuptools import setup

setup(
    name="viable_mapbox",
    version="1.0.0",
    description="Mapbox integration for Viable Cloud API",
    url="https://github.com/viableindustries/viable-integrations-mapbox",
    author="Viable Industries, L.L.C.",
    license="MIT",
    keywords="python setuptools package installer pip mapbox viablecloudapi",
    packages=["viable_mapbox"],
    include_package_data=True,
    install_requires=[
        "flask"
    ],
)
