import mapzen.whosonfirst.export

class importer(mapzen.whosonfirst.export.flatfile):

    def __init__(self, root, **kwargs):

        mapzen.whosonfirst.export.flatfile.__init__(self, root, **kwargs)

    def import_feature(self, feature):

        # as in mapzen.whosonfirst.export.flatfile.export_feature
        return self.export_feature(feature)
