import mapzen.whosonfirst.importer
import logging

class ne_importer(mapzen.whosonfirst.importer.base):

    def has_concordance(self, f):

        geom = mapzen.whosonfirst.utils.hash_geom(f)
        return self.has_concordance_lookup(geom, 'wof:geomhash')

class ne_marine_importer(ne_importer):

    def massage_feature(self, f):

        placetype = 'marinearea'

        if f['featurecla'] == 'ocean':
            placetype = 'ocean'

        props['src:geom'] = 'naturalearth'

        name = f['name']
        name = name.title()

        props['wof:name'] = name
        props['wof:placetype'] = placetype

        for k, v in props.items():

            if k.startswith("wof:"):
                continue

            new_k = "ne:%s" % k
            props[ new_k ] = v

            del(props[ k ])

        self.append_hierarchy_and_parent(f)
        # pass-by-ref
