#!/usr/bin/env python

from setuptools import setup, find_packages

packages = find_packages()
desc = open("README.md").read(),

setup(
    name='mapzen.whosonfirst.importer',
    namespace_packages=['mapzen', 'mapzen.whosonfirst', 'mapzen.whosonfirst.importer'],
    version='0.11',
    description='Simple Python wrapper for managing Who\'s On First import-related functions',
    author='Mapzen',
    url='https://github.com/thisisaaronland/py-mapzen-gazetter-import',
    install_requires=[
        'requests',
        'geojson',
        'mapzen.whosonfirst.export>=0.61',
        'mapzen.whosonfirst.concordances>=0.01',
        'mapzen.whosonfirst.spatial>=0.05',
        'mapzen.whosonfirst.pip>=0.02',
        'mapzen.whosonfirst.placetypes>=0.10',
        ],
    dependency_links=[
        'https://github.com/whosonfirst/py-mapzen-whosonfirst-export/tarball/master#egg=mapzen.whosonfirst.export-0.61',
        'https://github.com/whosonfirst/py-mapzen-whosonfirst-concordances/tarball/master#egg=mapzen.whosonfirst.concordances-0.01',
        'https://github.com/whosonfirst/py-mapzen-whosonfirst-spatial/tarball/master#egg=mapzen.whosonfirst.spatial-0.05',
        'https://github.com/whosonfirst/py-mapzen-whosonfirst-pip/tarball/master#egg=mapzen.whosonfirst.pip-0.02',
        'https://github.com/whosonfirst/py-mapzen-whosonfirst-pip/tarball/master#egg=mapzen.whosonfirst.placetypes-0.10',
        ],
    packages=packages,
    scripts=[
        'scripts/wof-importify'
        ],
    download_url='https://github.com/thisisaaronland/py-mapzen-whosonfirst-import/releases/tag/v0.11',
    license='BSD')
