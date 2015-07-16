# https://pythonhosted.org/setuptools/setuptools.html#namespace-packages
__import__('pkg_resources').declare_namespace(__name__)

import mapzen.whosonfirst.export

class base(mapzen.whosonfirst.export.flatfile):

    def __init__(self, root, **kwargs):

        mapzen.whosonfirst.export.flatfile.__init__(self, root, **kwargs)

    def import_feature(self, feature, **kwargs):

        # as in mapzen.whosonfirst.export.flatfile.export_feature
        return self.export_feature(feature, **kwargs)
