import mapzen.whosonfirst.importer

class qs_importer(mapzen.whosonfirst.importer.base):

    def massage_qs_properties(self, props):
        
        woeid = props.get('qs_woe_id', None)
        gnid = props.get('qs_gn_id', None)

        if woeid or gnid:

            concordances = {}
            
            if woeid:
                concordances['gp:id'] = woeid
            if gnid:
                concordances['gn:id'] = gnid

            props['wof:concordances'] = concordances

        iso = props.get('qs_iso_cc', None)

        if iso:
            del(props['qs_iso_cc'])
            props['iso:country'] = iso
            props['wof:country'] = iso

        for k, v in props.items():
            
            if k.startswith("qs_"):
                
                new_k = k.replace("qs_", "qs:")

                if v:                    
                    props[new_k] = v

                del(props[k])

        return props

# countries

class adm0_importer(qs_importer):

    def massage_feature(self, f):

        props = f['properties']
        
        # because there are no QS UIDS for countries...
        props['qs:id'] = props['qs_iso_cc']

        props['wof:name'] = props['qs_adm0']
        props['src:geom'] = 'quattroshapes'
        props['wof:placetype'] = 'country'

        props = self.massage_qs_properties(props)

        f['properties'] = props
        # pass-by-ref

# regions

class adm1_importer(qs_importer):

    def massage_feature(self, f):

        props = f['properties']

        props['src:geom'] = 'quattroshapes'
        props['wof:placetype'] = 'region'

        props['wof:name'] = props['qs_a1']

        props = self.massage_qs_properties(props)

        f['properties'] = props
        # pass-by-ref

# regions... but different... or something

class adm1_region_importer(qs_importer):

    def massage_feature(self, f):

        logging.error("WHY ARE YOU RUNNING THIS")
        sys.exit()

        props = f['properties']

        props['src:geom'] = 'quattroshapes'
        props['wof:placetype'] = 'region'	# DOUBLE CHECK

        props['wof:name'] = 'FIX ME'

        props = self.massage_qs_properties(props)

        f['properties'] = props
        # pass-by-ref

# counties (or whatever we end up calling them)

class adm2_importer(mapzen.whosonfirst.importer.base):

    def massage_feature(self, f):

        props = f['properties']

        props['src:geom'] = 'quattroshapes'
        props['wof:placetype'] = 'county'
        props['wof:name'] = props['qs_a2']

        props = self.massage_qs_properties(props)

        f['properties'] = props
        # pass-by-ref

# counties... but different... that are regions... or something

class adm2_region_importer(qs_importer):

    def massage_feature(self, f):

        logging.error("WHY ARE YOU RUNNING THIS")
        sys.exit()

        props = f['properties']

        props['src:geom'] = 'quattroshapes'
        props['wof:placetype'] = 'FIX ME'

        props['wof:name'] = 'FIX ME'

        props = self.massage_qs_properties(props)

        f['properties'] = props
        # pass-by-ref

# localadmins which are... what exactly

class localadmin_importer(qs_importer):

    def massage_feature(self, f):

        logging.error("WHY ARE YOU RUNNING THIS")
        sys.exit()

        props = f['properties']

        props['src:geom'] = 'quattroshapes'
        props['wof:placetype'] = 'FIX ME'

        props['wof:name'] = 'FIX ME'

        props = self.massage_qs_properties(props)

        f['properties'] = props
        # pass-by-ref

# localities

class locality_importer(qs_importer):

    def massage_feature(self, f):

        props = f['properties']

        props['src:geom'] = 'quattroshapes'
        props['wof:placetype'] = 'locality'
        props['wof:name'] = props['qs_loc']

        props = self.massage_qs_properties(props)

        f['properties'] = props
        # pass-by-ref

# neighbourhoods

class neighbourhood_importer(qs_importer):

    def massage_feature(self, f):

        props = f['properties']

        props['src:geom'] = 'quattroshapes'
        props['wof:placetype'] = 'neighbourhood'

        props['wof:name'] = props['name']

        props = self.massage_qs_properties(props)

        f['properties'] = props
        # pass-by-ref
