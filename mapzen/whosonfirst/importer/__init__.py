# https://pythonhosted.org/setuptools/setuptools.html#namespace-packages
__import__('pkg_resources').declare_namespace(__name__)

import logging

import shapely.geometry
import requests
import json
import random
import mapzen.whosonfirst.export
import mapzen.whosonfirst.spatial
import mapzen.whosonfirst.pip
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

        logging.error("I AM HERE")
        if not self.reversegeo:
            logging.warning("reverse geo is not enabled, can not append hierarchy")
            return

        qry = self.spatial_qry()
        qry.append_hierarchy_and_parent(feature)

        logging.error("WUB WUB WUB")

    def append_hierarchy_and_parent_pip(self, feature, **kwargs):

        props = feature['properties']
        placetype = props['wof:placetype']

        lat = props.get('geom:latitude', None)
        lon = props.get('geom:longitude', None)

        if not lat or not lon:

            shp = shapely.geometry.asShape(feature['geometry'])
            coords = shp.centroid

            lat = coords.y
            lon = coords.x

        # SEE THIS - THIS IS THE WORK
        # We are trying to figure out the hierarchy for a given placetype
        # which may have more than one immediate parent (for example a 
        # neighbourhood might be parented by a macrohood -or- a locality).
        # We are using the go-whosonfirst-pip server for this. See the way
        # we are hard-coding port numbers? So yeah... that is NOT the way
        # we want to keep doing this. On the other hand we're just trying to
        # get it to work at all right now so we'll live with it...

        all_servers = {
            'continent': 9999,
            'country': 7777,
            'region': 4444,
            'county': 3333,
            'locality': 6666,
            'macrohood': 2222,
            'neighbourhood': 5555,
        }

        pt = mapzen.whosonfirst.placetypes.placetype(placetype)

        _hiers = []

        for parent in pt.parents():

            parent = str(parent)
            port = all_servers.get(parent, None)

            if not port:
                logging.error("OH NO... CAN NOT FIND PIP PORT FOR %s" % parent)
                sys.exit()

            server = mapzen.whosonfirst.pip.server(port=port)

            # TO DO: some kind of 'ping' to make sure the server is actually
            # there... (20151221/thisisaaronland)

            rsp = server.reverse_geocode(lat, lon)

            if len(rsp):
                _rsp = rsp
                break

        for r in _rsp:
            id = r['Id']
            pf = mapzen.whosonfirst.utils.load(self.root, id)
            pp = pf['properties']
            ph = pp['wof:hierarchy']

            for h in ph:

                # k = "%s_id" % placetype
                # h[k] = wofid
                _hiers.append(h)

        if len(_rsp) == 0:
            logging.warning("Failed to reverse geocode any parents for %s, %s" % (lat, lon))
            return False

        if len(_rsp) != 1:  
            logging.warning("Multiple reverse geocoding possibilities %s, %s" % (lat, lon))
            return False

        if len(_hiers) == 0:
            return True

        parent_id = _rsp[0]['Id']
        props['wof:parent_id'] = parent_id

        props['wof:hierarchy'] = _hiers
        feature['properties'] = props

        return True
        
