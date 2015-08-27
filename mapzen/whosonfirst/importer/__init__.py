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

        if kwargs.get('reversegeo', False):

            self.reversegeo = True

            spatial_dsn = kwargs.get('reversegeo_dsn', None)
            spatial_qry = mapzen.whosonfirst.spatial.query(spatial_dsn)

            self.spatial_qry = spatial_qry

    def import_feature(self, feature, **kwargs):

        if self.has_concordance(feature):
            logging.debug("already has concordance, skipping")
            return True

        # as in mapzen.whosonfirst.export.flatfile.export_feature

        return self.export_feature(feature, **kwargs)
        
    # this is left to individual packages to implement; it is 
    # assumed that most of them will call has_concordance_lookup
    # below (20150826/thisisaaronland)

    def has_concordance(self, f):
        return False

    def has_concordance_lookup(self, other_id, other_src):

        # this assumes you've checked that concordances are
        # enabled already (20150826/thisisaaronland)

        row = self.concordances_qry.by_other_id(other_id, other_src)

        if row:
            return True

        return False

    def append_hierarchy_and_parent(self, feature, **kwargs):

        self.append_hierarchy(feature, **kwargs)

        parent_id = -1

        props = feature['properties']
        hier = props['wof:hierarchy']
        count = len(hier)

        if count == 0:
            logging.warning("failed to assign hierarchy so there's nothing to derive parents from")
            
        elif count > 1:
            logging.warning("too many parents to choose from")

        else:

            h = hier[0]

            placetype = props['wof:placetype']
            placetype = mapzen.whosonfirst.placetypes.placetype(placetype)

            # file under known-knowns : some (many?) venues may not have
            # available neighbourhood polygons at the time of their import
            # so rather than changing the placetype spec and allowing
            # localities to parent venues we're just going to mark the 
            # parent ID as -1 and deal with it later once we've imported
            # more data (20150826/thisisaaronland)

            for p in placetype.parents():
            
                k = "%s_id" % p

                if h.get(k, None):
                    parent_id = h[k]
                    break

        props['wof:parent_id'] = parent_id
        feature['properties'] = props

    # note this is out of sync with mapzen.whosonfirst.utils.generate_hierarchy
    # which calls the remote API endpoint (21050826/thisisaaronland)
    
    def append_hierarchy(self, feature, **kwargs):

        hier = []

        props = feature['properties']

        geom = feature['geometry']
        shp = shapely.geometry.asShape(geom)
        coords = shp.centroid

        lat = coords.y
        lon = coords.x

        placetypes = ('neighbourhood', 'locality', 'region', 'country')
        rsp = self.spatial_qry.get_by_latlon_recursive(lat, lon, placetypes=placetypes)

        # See this - we're doing it this way just to maintain parity with the
        # (current) reversegeo remote API endpoint (20150826/thisisaaronland)

        data = { 'features': list(rsp) }

        """
        placetype = ('neighbourhood', 'locality', 'region', 'country')
        placetype = ",".join(placetype)

        try:
            params = {'latitude': lat, 'longitude': lon, 'placetype': placetype}
            rsp = requests.get('https://54.148.56.3/', params=params, verify=False)
                
            data = json.loads(rsp.content)
        except Exception, e:
            logging.error(e)
            return
        """

        if len(data['features']) == 1:
            props['wof:parent_id'] = data['features'][0]['id']

        if len(data['features']) >= 1:

            for pf in data['features']:
                pp = pf['properties']

                if pp.get('wof:hierarchy', False):
                    hier.extend(pp['wof:hierarchy'])

        props['wof:hierarchy'] = hier
        feature['properties'] = props
        
