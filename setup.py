#!/usr/bin/env python

from setuptools import setup, find_packages

packages = find_packages()
desc = open("README.md").read(),

setup(
    name='mapzen.whosonfirst.importer',
    namespace_packages=['mapzen', 'mapzen.whosonfirst', 'mapzen.whosonfirst.importer'],
    version='0.03',
    description='Simple Python wrapper for managing Who\'s On First import-related functions',
    author='Mapzen',
    url='https://github.com/thisisaaronland/py-mapzen-gazetter-import',
    install_requires=[
        'requests',
        'geojson',
        'mapzen.whosonfirst.export',
        'mapzen.whosonfirst.concordances',
        'mapzen.whosonfirst.spatial',
        ],
    dependency_links=[
        'https://github.com/mapzen/py-mapzen-whosonfirst-export/tarball/master#egg=mapzen-whosonfirst-export-0.39',
        ],
    packages=packages,
    scripts=[
        ],
    download_url='https://github.com/thisisaaronland/py-mapzen-whosonfirst-import/releases/tag/v0.03',
    license='BSD')
