# https://pythonhosted.org/setuptools/setuptools.html#namespace-packages
__import__('pkg_resources').declare_namespace(__name__)

import mapzen.whosonfirst.export

import shapely.geometry
import requests
import json

class base(mapzen.whosonfirst.export.flatfile):

    def __init__(self, root, **kwargs):

        mapzen.whosonfirst.export.flatfile.__init__(self, root, **kwargs)

    def import_feature(self, feature, **kwargs):

        if self.concordances_db:

            # Note this is *before* we have massage_feature-ed
            # the feature so the ID will be bound to the properties
            # and not a 'wof:concordances' property

            lookup = props.get(self.concordances_key, None)

            if lookup:
                wofid = self.concordances_db.woe_id(lookup)
                logging.debug("got %s for %s" % (wofid, lookup))

                if wofid != 0:
                    return True

        # as in mapzen.whosonfirst.export.flatfile.export_feature

        return self.export_feature(feature, **kwargs)

    # maybe put this in mapzen.whosonfirst.export as 'ensure_hierarchy' ?
    # (20150727/thisisaaronland)

    def append_hierarchy(self, feature, **kwargs):

        props = feature['properties']

        hier = []

        geom = f['geometry']
        shp = shapely.geometry.asShape(geom)
        coords = shp.centroid

        lat = coords.y
        lon = coords.x

        for pt in ('neighbourhood', 'locality', 'region', 'country'):

            try:
                params = {'latitude': lat, 'longitude': lon, 'placetype': pt}
                rsp = requests.get('https://54.148.56.3/', params=params, verify=False)
                
                data = json.loads(rsp.content)
            except Exception, e:
                logging.error(e)
                continue

            if len(data['features']) == 1:
                props['wof:parent_id'] = data['features'][0]['id']

            if len(data['features']) >= 1:

                for pf in data['features']:
                    pp = pf['properties']

                    if pp.get('wof:hierarchy', False):
                        hier.extend(pp['wof:hierarchy'])

                break

        props['wof:hierarchy'] = hier

        feature['properties'] = props
        
