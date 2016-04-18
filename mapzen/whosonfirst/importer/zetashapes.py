class importer:

    def massage_feature(f):

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
