# https://pythonhosted.org/setuptools/setuptools.html#namespace-packages
__import__('pkg_resources').declare_namespace(__name__)

import logging

import shapely.geometry
import requests
import json
import random
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
            self.spatial_dsn = spatial_dsn

            # because this: http://initd.org/psycopg/docs/usage.html#thread-safety

            self.spatial_qry_maxconns = 20
            self.spatial_qry_conns = []

    def spatial_qry(self):

        if len(self.spatial_qry_conns) < self.spatial_qry_maxconns:

            conn = mapzen.whosonfirst.spatial.query(self.spatial_dsn)
            self.spatial_qry_conns.append(conn)

            logging.debug("return new spatial query connection")
            return conn

        logging.debug("return existing spatial query connection")

        random.shuffle(self.spatial_qry_conns)
        return self.spatial_qry_conns[0]

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

        qry = self.concordances_qry()
        row = qry.by_other_id(other_id, other_src)

        if row:
            return row

        return None

    def append_hierarchy_and_parent(self, feature, **kwargs):

        if not self.reversegeo:
            logging.warning("reverse geo is not enabled, can not append hierarchy")
            return

        qry = self.spatial_qry()
        qry.append_hierarchy_and_parent(feature)
