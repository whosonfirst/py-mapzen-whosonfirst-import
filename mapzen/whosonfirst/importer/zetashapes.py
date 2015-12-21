import mapzen.whosonfirst.importer
import logging

class importer(mapzen.whosonfirst.importer.base):

    def has_concordance(self, f):

        if not self.concordances:
            return False
            
        other_src = self.concordances_key
        other_id = f['properties']['id']

        return self.has_concordance_lookup(other_id, other_src)

    def massage_feature(self, f):

        props = f['properties']
        id = int(props['id'])

        for k, v in props.items():
            zs_k = "zs:%s" % k
            props[zs_k] = v
            del(props[k])
            
        props['src:geom'] = 'zetashapes'

        props['wof:placetype'] = 'neighbourhood'
        props['wof:parent_id'] = -1

        if props.get('zs:label', None):
            props['wof:name'] = props['zs:label']

        concordances = props.get('wof:concordances', {})
        concordances['gp:id'] = id

        props['wof:concordances'] = concordances

        f['properties'] = props

        self.append_hierarchy_and_parent_pip(f)
