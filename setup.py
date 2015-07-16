#!/usr/bin/env python

from setuptools import setup, find_packages

packages = find_packages()
desc = open("README.md").read(),

setup(
    name='mapzen.whosonfirst.importer',
    namespace_packages=['mapzen', 'mapzen.whosonfirst', 'mapzen.whosonfirst.importer'],
    version='0.01',
    description='Simple Python wrapper for managing Who\'s On First import-related functions',
    author='Mapzen',
    url='https://github.com/thisisaaronland/py-mapzen-gazetter-import',
    install_requires=[
        'requests',
        'geojson',
        'woe.isthat',
        # 'address_normalizer',
        'mapzen.whosonfirst.export',
        ],
    dependency_links=[
        # 'https://github.com/openvenues/address_normalizer/tarball/master#egg=address-normalizer-0.2',
        'https://github.com/thisisaaronland/py-woe-isthat/tarball/master#egg=woe-isthat-0.15',
        'https://github.com/mapzen/py-mapzen-whosonfirst-export/tarball/master#egg=mapzen-whosonfirst-export-0.39',
        ],
    packages=packages,
    scripts=[
        ],
    download_url='https://github.com/thisisaaronland/py-mapzen-whosonfirst-import/releases/tag/v0.01',
    license='BSD')
