# https://pythonhosted.org/setuptools/setuptools.html#namespace-packages
__import__('pkg_resources').declare_namespace(__name__)

import logging

import shapely.geometry
import requests
import json

import mapzen.whosonfirst.export
import mapzen.whosonfirst.spatial
import mapzen.whosonfirst.placetypes

class base(mapzen.whosonfirst.export.flatfile):

    def __init__(self, root, **kwargs):

        mapzen.whosonfirst.export.flatfile.__init__(self, root, **kwargs)

        self.reversegeo = False

        reversegeo = kwargs.get('reversegeo', False)
        logging.debug("enable reversegeo: %s" % reversegeo)

        if reversegeo:

            self.reversegeo = True

            spatial_dsn = kwargs.get('reversegeo_dsn', None)
            spatial_qry = mapzen.whosonfirst.spatial.query(spatial_dsn)

            self.spatial_qry = spatial_qry

    def import_feature(self, feature, **kwargs):

        concordance = self.has_concordance(feature)

        if concordance:

            # this is a little bit of hoop-jumping to make
            # the reporting messages make a little more sense
            # (20150902/thisisaaronland)

            wofid = concordance[0]
            feature['id'] = wofid
            feature['properties']['wof:id'] = wofid

            path = self.feature_path(feature)
            logging.debug("already has concordance (%s) skipping" % path)
            return path

        # as in mapzen.whosonfirst.export.flatfile.export_feature

        path = self.export_feature(feature, **kwargs)
        return path
        
    # this is left to individual packages to implement; it is 
    # assumed that most of them will call has_concordance_lookup
    # below (20150826/thisisaaronland)

    def has_concordance(self, f):
        return None

    def has_concordance_lookup(self, other_id, other_src):

        # this assumes you've checked that concordances are
        # enabled already (20150826/thisisaaronland)

        row = self.concordances_qry.by_other_id(other_id, other_src)

        if row:
            return row

        return None

    def append_hierarchy_and_parent(self, feature, **kwargs):

        if not self.reversegeo:
            logging.warning("reverse geo is not enabled, can not append hierarchy")
            return

        self.spatial_qry.append_hierarchy_and_parent(feature)
