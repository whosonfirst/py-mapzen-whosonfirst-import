import mapzen.whosonfirst.importer
import logging

class qs_importer(mapzen.whosonfirst.importer.base):

    def has_concordance(self, f):

        geom = mapzen.whosonfirst.utils.hash_geom(f)
        return self.has_concordance_lookup(geom, 'wof:geomhash')

    # Note this is just properties - we end up calling
    # self.append_hierarchy_and_parent(f) over and over
    # below because (f)eature and because I can't be 
    # bothered to add YA meta wrapper thingy right now
    # (20151012/thisisaaronland)

    def massage_qs_properties(self, props):

        # See below in the "concordances" importer

        concordances = props.get('wof:concordances', {})

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

# concordances (because whatever) seriously don't spend any time thinking
# about the name... it's just the history of QS...it's not a big deal
# see also: quattroshapes_gazetteer_gp_then_gn.geojson
# see also-er: https://github.com/whosonfirst/whosonfirst-data/issues/107

class concordances_importer(mapzen.whosonfirst.importer.base):

    def has_concordance(self, f):

        # BUT WAIT! IF I AM THE "CONCORDANCES" FILE (see below)
        # THEN WE FIRST NEED TO CHECK qs:id and gp:id (WOE) and
        # then gn:id BECAUSE SOME OF THEM HAVE ALREADY BEEN IMPORTED. FOR
        # EXAMPLE: https://whosonfirst.mapzen.com/spelunker/id/85864475/
        # (20151030/thisissaaronland)

        props = f['properties']

        for other_src in ('qs_id', 'woe_id', 'gn_id'):

            if not props.get(other_src, False):
                continue

            other_id = props[other_src]

            has_c = self.has_concordance_lookup(other_id, other_src)
            logging.debug("HAS %s:%s concordance %s" % (other_src, other_id, has_c))

            if has_c:
                return True

        geom = mapzen.whosonfirst.utils.hash_geom(f)
        return self.has_concordance_lookup(geom, 'wof:geomhash')

    def massage_feature(self, f):

        props = f['properties']

        props['wof:name'] = props['name']
        props['wof:source'] = 'quattroshapes'
        props['qs:source'] = 'gazetteer'

        if props['placetype'] == 'Suburb':
            props['wof:placetype'] = 'neighbourhood'
        else:
            props['wof:placetype'] = 'locality'	# because "unitary local admin" ... whatever that is (talk to kelso)

        concordances = props.get('wof:concordances', {})

        if props.get('qs_id', False):
            concordances['qs:id'] = props['qs_id']

        if props.get('woe_id', False):
            concordances['gp:id'] = props['woe_id']

        if props.get('gn_id', False):
            concordances['gn:id'] = props['gn_id']

        if len(concordance.keys()) > 0:
            props['wof:concordances'] = concordances

        props = self.massage_qs_properties(props)
        f['properties'] = props

        self.append_hierarchy_and_parent(f)

        f['properties'] = props
        # pass-by-ref

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

        try:
            name = name.title()
        except Exception, e:
            pass

        props['wof:name'] = name

        alt = props.get('qs_a1r_alt', '')

        try:
            if alt != None and alt != '':
                alt = alt.title()
                props['name:und_x_variant'] = [ alt ]
        except Exception, e:
            pass

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

        props = f['properties']

        props['src:geom'] = 'quattroshapes'
        props['wof:placetype'] = 'macrocounty'

        name = props.get('qs_a2r', '')
        name = name.title()

        props['wof:name'] = name

        alt = props.get('qs_a2r_alt', '')

        try:
            if alt != None and alt != '':
                alt = alt.title()
                props['name:und_x_variant'] = [ alt ]
        except Exception, e:
            pass

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
        
        try:
            name = name.title()
        except Exception, e:
            pass

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
