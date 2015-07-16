import mapzen.whosonfirst.import

class timezone_importer(mapzen.whosonfirst.import.importer):

    def massage_feature(self, f):

        woe_props = f['properties']

        props = {}
        props['wof:placetype'] = 'timezone'
        props['wof:source'] = 'woedb'
        props['wof:name'] = woe_props.get('name', '')
        props['wof:fullname'] = woe_props.get('fullname', '')
        props['woe:id'] = woe_props.get('woe:id', 0)

        if woe_props.get('provider', False):
            props['woe:source'] = woe_props['provider']

        f['properties'] = props
