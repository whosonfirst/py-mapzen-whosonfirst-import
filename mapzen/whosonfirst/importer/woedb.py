import mapzen.whosonfirst.importer

class timezone_importer(mapzen.whosonfirst.importer.base):

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


class airport_importer(mapzen.whosonfirst.importer.base):

    def massage_feature(self, f):

        woe_props = f['properties']

        props = {}
        props['wof:placetype'] = 'campus'
        props['wof:source'] = 'woedb'
        props['wof:name'] = woe_props.get('name', '')

        props['wof:parent_id'] = -1

        if woe_props.get('fullname', None) :
            props['wof:fullname'] = woe_props['wof:fullname']

        concordances = {}

        for k in ('woe:id', 'iata:code', 'icao:code'):

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

        for k, v in woe_props.get('hierarchy', {}):
            k = "%s_id" % k
            woe_hier[k] = v

        if len(woe_hier.keys()):
            props['woe:hierarchy'] = woe_hier


        f['properties'] = props

        self.append_hierarchy(f)
