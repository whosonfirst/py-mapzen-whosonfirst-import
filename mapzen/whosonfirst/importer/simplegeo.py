import mapzen.whosonfirst.importer
import logging

class importer(mapzen.whosonfirst.importer.base):

    def has_concordance(self, f):

        if not self.concordances:
            return False
            
        other_src = self.concordances_key
        other_id = f['id']

        return self.has_concordance_lookup(other_id, other_src)

    def massage_feature(self, f):

        sgid = f.get('id', None)

        if sgid:
            del(f['id'])

        props = f['properties']

        for k, v in props.items():
            sg_k = "sg:%s" % k
            props[sg_k] = v
            del(props[k])
            
        props['src:geom'] = 'simplegeo'

        props['wof:placetype'] = 'venue'
        props['wof:parent_id'] = -1

        if props.get('sg:name', None):
            props['wof:name'] = props['sg:name']
            del(props['sg:name'])

        if props.get('sg:country', None):
            props['iso:country'] = props['sg:country']
            del(props['sg:country'])

        if sgid:
            concordances = props.get('wof:concordances', {})
            concordances['sg:id'] = sgid

            props['wof:concordances'] = concordances

        f['properties'] = props

        self.append_hierarchy(f)

        logging.debug(props)
