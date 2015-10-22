import mapzen.whosonfirst.importer
import logging

class ne_importer(mapzen.whosonfirst.importer.base):

    def has_concordance(self, f):

        geom = mapzen.whosonfirst.utils.hash_geom(f)
        return self.has_concordance_lookup(geom, 'wof:geomhash')

class marine_importer(ne_importer):

    def massage_feature(self, f):

        props = f['properties']

        placetype = 'marinearea'

        if props['featurecla'] == 'ocean':
            placetype = 'ocean'

        props['src:geom'] = 'naturalearth'

        name = props['name']

        if name == None:
            name = ""
        else:
            name = name.title()

        props['wof:name'] = name
        props['wof:placetype'] = placetype

        for k, v in props.items():

            if k.startswith("wof:"):
                continue

            new_k = "ne:%s" % k
            props[ new_k ] = v

            del(props[ k ])

        f['properties'] = props

        self.append_hierarchy_and_parent(f)

        if placetype == 'ocean' and f['properties']['wof:parent_id'] == -1:
            f['properties']['wof:parent_id'] = 0
            f['properties']['wof:hierarchy'] = [ { 'planet_id': 0 } ]

        # pass-by-ref
