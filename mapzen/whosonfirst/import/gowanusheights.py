import mapzen.whosonfirst.import

class importer(mapzen.whosonfirst.import.importer):

    def massage_feature(self, f):

        props = {}
        props['wof:placetype'] = 'neighbourhood'
        props['wof:source'] = 'woedb'
        props['iso:country'] = 'US'
        props['wof:name'] = 'Gowanus Heights'
        props['woe:id'] = 18807771

        f['properties'] = props
