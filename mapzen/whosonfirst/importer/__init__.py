# https://pythonhosted.org/setuptools/setuptools.html#namespace-packages
__import__('pkg_resources').declare_namespace(__name__)

import mapzen.whosonfirst.export
import logging

import shapely.geometry
import requests
import json

class base(mapzen.whosonfirst.export.flatfile):

    def __init__(self, root, **kwargs):

        mapzen.whosonfirst.export.flatfile.__init__(self, root, **kwargs)

    def import_feature(self, feature, **kwargs):

        if self.has_concordance(feature):
            logging.debug("already has concordance, skipping")
            return True

        # as in mapzen.whosonfirst.export.flatfile.export_feature

        return self.export_feature(feature, **kwargs)
        
    # this is left to individual packages to implement
    # (20150826/thisisaaronland)

    def has_concordance(self, f):
        return False

    def has_concordance_lookup(self, other_id, other_src):

        # this assumes you've checked that concordances are
        # enabled already (20150826/thisisaaronland)

        row = self.concordances_qry.by_other_id(other_id, other_src)

        if row:
            return True

        return False

    # maybe put this in mapzen.whosonfirst.export as 'ensure_hierarchy' ?
    # (20150727/thisisaaronland)

    # please to update me to use mapzen.whosonfirst.utils.generate_hierarchy
    # (21050807/thisisaaronland)
    
    def append_hierarchy(self, feature, **kwargs):

        hier = []

        props = feature['properties']

        geom = feature['geometry']
        shp = shapely.geometry.asShape(geom)
        coords = shp.centroid

        lat = coords.y
        lon = coords.x
        
        # this assumes a copy of py-mapzen-whosonfirst-lookup with
        # recursive get_by_latlon (20150728/thisisaaronland)

        # TO DO: replace with py-mapzen-whosonfirst-spatial
        # (20150826/thisisaaronland)

        placetype = ('neighbourhood', 'locality', 'region', 'country')
        placetype = ",".join(placetype)

        try:
            params = {'latitude': lat, 'longitude': lon, 'placetype': placetype}
            rsp = requests.get('https://54.148.56.3/', params=params, verify=False)
                
            data = json.loads(rsp.content)
        except Exception, e:
            logging.error(e)
            return

        if len(data['features']) == 1:
            props['wof:parent_id'] = data['features'][0]['id']

        if len(data['features']) >= 1:

            for pf in data['features']:
                pp = pf['properties']

                if pp.get('wof:hierarchy', False):
                    hier.extend(pp['wof:hierarchy'])

        props['wof:hierarchy'] = hier

        feature['properties'] = props
        
