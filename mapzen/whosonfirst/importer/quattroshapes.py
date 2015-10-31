import mapzen.whosonfirst.importer
import woe.isthat

# concordances (because whatever)
# seriously don't spend any time thinking about the name... it's just
# the history of QS...it's not a big deal
# see also: quattroshapes_gazetteer_gp_then_gn.geojson

class concordances_importer(mapzen.whosonfirst.importer.base):

    def massage_feature(self, f):

        props = f['properties']
        
        props['qs:id'] = props['qs_id']

        props['wof:name'] = props['name']
        props['wof:source'] = 'quattroshapes'
        props['qs:source'] = 'gazetteer'
        props['wof:placetype'] = 'locality'	# because "unitary local admin" ... whatever that is (talk to kelso)

        concordances = {}

        if props.get('woe_id', False):
            concordances['gp:id'] = props['woe_id']

        if props.get('gn_id', False):
            concordances['gn:id'] = props['gn_id']

        if len(concordance.keys()) > 0:
            props['wof:concordances'] = concordances

        f['properties'] = props
        # pass-by-ref

# countries

class adm0_importer(mapzen.whosonfirst.importer.base):

    def massage_feature(self, f):

        props = f['properties']
        
        # because there are no QS UIDS for countries...
        props['qs:id'] = props['qs_iso_cc']

        props['wof:name'] = props['qs_adm0']
        props['wof:source'] = 'quattroshapes'
        props['wof:placetype'] = 'country'

        f['properties'] = props
        # pass-by-ref

# regions

class adm1_importer(mapzen.whosonfirst.importer.base):

    # note - this needs to be taught how to deal with adm1_region
    # thingies from quattroshapes (20150625/thisisaaronland)

    def massage_feature(self, f):

        props = f['properties']

        props['src:geom'] = 'quattroshapes'
        props['wof:placetype'] = 'region'

        props['wof:name'] = props['qs_a1']

        woeid = props.get('qs_woe_id', None)

        """
        if woeid:
            props['woe:id'] = woeid
        """

        iso = props.get('qs_iso_cc', None)

        if iso:
            props['iso:country'] = iso

        f['properties'] = props
        # pass-by-ref

# counties (or whatever we end up calling them)

class adm2_importer(mapzen.whosonfirst.importer.base):

    def massage_feature(self, f):

        props = f['properties']

        props['wof:source'] = 'quattroshapes'
        props['wof:placetype'] = 'county'

        props['wof:name'] = props['qs_a2']

        woeid = props.get('qs_woe_id', None)
        gnid = props.get('qs_gn_id', None)

        if woeid:
            props['woe:id'] = woeid

        iso = props.get('qs_iso_cc', None)

        if iso:
            del(props['qs_iso_cc'])
            props['iso:country'] = iso

        for k, v in props.items():
            
            if k.startswith("qs_"):
                
                new_k = k.replace("qs_", "qs:")

                if v:                    
                    props[new_k] = v

                del(props[k])

        f['properties'] = props
        # pass-by-ref

# localities

class locality_importer(mapzen.whosonfirst.importer.base):

    def massage_feature(self, f):

        props = f['properties']

        props['wof:source'] = 'quattroshapes'
        props['wof:placetype'] = 'locality'
        props['wof:name'] = props['qs_loc']

        woeid = props.get('qs_woe_id', None)

        if woeid:
            props['woe:id'] = woeid

        gnid = props.get('qs_gn_id', None)

        if gnid:
            props['geonames:id'] = gnid

        # because stuff like this - u'qs_iso_cc': u'U',
        # (20150626/thisisaaronland)

        iso = props.get('qs_iso_cc', None)

        if iso and len(iso) == 2:
            props['iso:country'] = iso

        f['properties'] = props
        # pass-by-ref

# neighbourhoods

class neighbourhood_importer(mapzen.whosonfirst.importer.base):

    def massage_feature(self, f):

        props = f['properties']

        props['wof:source'] = 'quattroshapes'
        props['wof:placetype'] = 'neighbourhood'

        props['wof:name'] = props['name']

        woeid = props.get('woe_id', None)

        if woeid:
            props['woe:id'] = woeid

        gnid = props.get('gn_id', None)

        if gnid:
            props['geonames:id'] = gnid

        f['properties'] = props
        # pass-by-ref
