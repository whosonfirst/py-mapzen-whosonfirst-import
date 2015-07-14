import mapzen.whosonfirst.import

class importer(mapzen.whosonfirst.import.importer):

    def massage_feature(self, f):

        props = {}
        props['wof:placetype'] = 'neighbourhood'
        props['iso:country'] = 'US'
        props['wof:name'] = 'La Lengua'

        f['properties'] = props
