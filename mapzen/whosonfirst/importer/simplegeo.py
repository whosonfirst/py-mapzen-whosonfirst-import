import mapzen.whosonfirst.importer
import logging

def massage_feature(f):

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

    # see also:
    # https://github.com/whosonfirst/whosonfirst-sources/issues/2
    
    if props.get('sg:href', None):
        del(props['sg:href'])
        
    if sgid:
        concordances = props.get('wof:concordances', {})
        concordances['sg:id'] = sgid
        
        props['wof:concordances'] = concordances

    tags = props.get('sg:tags', [])
    props['wof:tags'] = tags
    
    f['properties'] = props

