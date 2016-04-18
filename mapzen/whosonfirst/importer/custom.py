class gowanusheights_importer:

    def massage_feature(f):

        props = {}
        props['wof:placetype'] = 'neighbourhood'
        props['wof:source'] = 'woedb'
        props['iso:country'] = 'US'
        props['wof:name'] = 'Gowanus Heights'
        props['woe:id'] = 18807771

        f['properties'] = props

class lalengua_importer:

    def massage_feature(f):

        props = {}
        props['wof:placetype'] = 'neighbourhood'
        props['iso:country'] = 'US'
        props['wof:name'] = 'La Lengua'

        f['properties'] = props

class minitenders_importer:

    def massage_feature(f):

        name = f['properties']['Name']

        props = {}
        props['wof:placetype'] = 'microhood'
        props['iso:country'] = 'US'
        props['wof:parent_id'] = 85865903
        props['wof:belongsto'] = [85865903, 85688637, 85922583, 85633793, 102087579]
        props['wof:name'] = name
        props['name:eng_p'] = [ name ]

        f['properties'] = props
