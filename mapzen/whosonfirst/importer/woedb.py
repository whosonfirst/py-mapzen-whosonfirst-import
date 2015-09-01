import mapzen.whosonfirst.importer
import logging

class woedb_importer(mapzen.whosonfirst.importer.base):

    def has_concordance(self, f):

        if not self.concordances_db:
            return False
            
        props = f['properties']
        lookup = props['woe:id']

        if lookup:
            wofid = self.concordances_db.woe_id(lookup)
            logging.debug("got %s for %s" % (wofid, lookup))

        if wofid == 0:
            return False

        return True
    
class timezone_importer(woedb_importer):

    def massage_feature(self, f):

        woe_props = f['properties']

        props = {}
        props['src:geom'] = 'woedb'
        props['wof:placetype'] = 'timezone'
        props['wof:name'] = woe_props.get('name', '')
        props['wof:fullname'] = woe_props.get('fullname', '')
        props['woe:id'] = woe_props.get('woe:id', 0)

        if woe_props.get('provider', False):
            props['woe:source'] = woe_props['provider']

        f['properties'] = props


class airport_importer(woedb_importer):

    def massage_feature(self, f):

        woe_props = f['properties']

        props = {}
        props['wof:placetype'] = 'campus'
        props['wof:name'] = woe_props.get('name', '')

        props['src:geom'] = 'woedb'

        woe_geom = f['geometry']
        
        if woe_geom['type'] == 'Polygon':

            coords = woe_geom['coordinates'][0]
            count = len(coords)

            if count == 5:
                logging.warning("%s only has 5 coords, a bounding box" % props['wof:name'])

                f['geometry'] = {
                    'type': 'Point',
                    'coordinates': [ 0, 0 ]
                }

                props['src:geom'] = 'missing'

        props['wof:parent_id'] = -1

        if woe_props.get('fullname', None) :
            props['wof:fullname'] = woe_props['fullname']

        concordances = {}

        for k in ('woe:id', 'iata:code', 'icao:code', 'faa:code', 'geonames:id'):

            if woe_props.get(k, False):
                concordances[k] = woe_props[k]

        props['wof:concordances'] = concordances

        if woe_props.get('provider', False):
            props['woe:source'] = woe_props['provider']

        if woe_props.get('iso', False):
            props['iso_country'] = woe_props['iso']
            
        for k, v in woe_props.items():

            if not k.startswith("alias"):
                continue

            k = k.lower()

            ignore, lang, flag = k.split("_")

            if flag == "q":
                flag = "p"

            k = "name:%s_%s" % (lang, flag)

            props[k] = v

        #

        woe_hier = {}

        for k in woe_props.get('hierarchy', []):

            k,v = k.split("=")

            k = k.replace("woe:", "")
            k = "%s_id" % k

            v = int(v)

            woe_hier[k] = v

        if len(woe_hier.keys()):
            props['woe:hierarchy'] = woe_hier

        f['properties'] = props

        self.append_hierarchy_and_parent(f)
        
