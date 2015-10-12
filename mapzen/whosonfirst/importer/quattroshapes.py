import mapzen.whosonfirst.importer

class qs_importer(mapzen.whosonfirst.importer.base):

    # Note this is just properties - we end up calling
    # self.append_hierarchy_and_parent(f) over and over
    # below because (f)eature and because I can't be 
    # bothered to add YA meta wrapper thingy right now
    # (20151012/thisisaaronland)

    def massage_qs_properties(self, props):

        concordances = {}

        qsid = props.get('qs_id', None)
        woeid = props.get('qs_woe_id', None)
        gnid = props.get('qs_gn_id', None)

        if woeid or gnid or qsid:

            
            if qsid:
                concordances['qs:id'] = qsid

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

        self.append_hierarchy_and_parent(f)
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

        self.append_hierarchy_and_parent(f)
        # pass-by-ref

# macroregions

class adm1_region_importer(qs_importer):

    def massage_feature(self, f):

        props = f['properties']

        props['src:geom'] = 'quattroshapes'
        props['wof:placetype'] = 'macroregion' 

        name = props.get('qs_a1r', '')
        name = name.title()

        props['wof:name'] = name

        alt = props.get('qs_a1r_alt', '')

        if alt != None and alt != '':
            alt = alt.title()
            props['name:und_x_variant'] = [ alt ]

        props = self.massage_qs_properties(props)
        f['properties'] = props

        self.append_hierarchy_and_parent(f)
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

        self.append_hierarchy_and_parent(f)
        # pass-by-ref

# macrocounties

class adm2_region_importer(qs_importer):

    def massage_feature(self, f):

        logging.error("WHY ARE YOU RUNNING THIS")
        sys.exit()

        props = f['properties']

        props['src:geom'] = 'quattroshapes'
        props['wof:placetype'] = 'macrocounty'

        name = props.get('qs_a2r', '')
        name = name.title()

        props['wof:name'] = name

        alt = props.get('qs_a2r_alt', '')

        if alt != None and alt != '':
            alt = alt.title()
            props['name:und_x_variant'] = [ alt ]

        props = self.massage_qs_properties(props)
        f['properties'] = props

        self.append_hierarchy_and_parent(f)
        # pass-by-ref

# localadmins

class localadmin_importer(qs_importer):

    def massage_feature(self, f):

        props = f['properties']

        props['src:geom'] = 'quattroshapes'
        props['wof:placetype'] = 'localadmin'

        name = props.get('qs_la', '')
        name = name.title()

        alt = props.get('qs_la_alt', '')

        props['wof:name'] = name

        if alt != None and alt != '':
            alt = alt.title()
            props['name:und_x_variant'] = [ alt ]

        props = self.massage_qs_properties(props)
        f['properties'] = props

        self.append_hierarchy_and_parent(f)
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

        self.append_hierarchy_and_parent(f)
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

        self.append_hierarchy_and_parent(f)
        # pass-by-ref
