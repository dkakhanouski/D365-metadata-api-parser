import json
from pprint import pprint

# # get relationships definition from json
# rdjson = json.load(open('C:\\Users\\dkakhanouski\\Documents\\RelationshipDefinitions.json'))
# rdmeta = rdjson['value']
# # get entity relationships
# er = list(map(lambda x: {'ReferencedAttribute' :x.get('ReferencedAttribute'),\
#                          'ReferencedEntity'    :x.get('ReferencedEntity'),\
#                          'ReferencingAttribute':x.get('ReferencingAttribute'),\
#                          'ReferencingEntity'   :x.get('ReferencingEntity')}, rdmeta))
# refed = {x.get('ReferencedEntity') : x for x in er}
# refing = {x.get('ReferencingEntity') : x for x in er}
# pprint(refed.get('account'))
# pprint(refing.get('account'))

def get_referenced_entities(entity_name):
  # get relationships definition from json
  rdjson = json.load(open('C:\\Users\\dkakhanouski\\Documents\\RelationshipDefinitions.json'))
  rdmeta = rdjson['value']
  # get entities relationships
  er = list(map(lambda x: {'ReferencedAttribute' :x.get('ReferencedAttribute'),\
                           'ReferencedEntity'    :x.get('ReferencedEntity'),\
                           'ReferencingAttribute':x.get('ReferencingAttribute'),\
                           'ReferencingEntity'   :x.get('ReferencingEntity')}, rdmeta))
  # get all referenced entities
  re = [(x.get('ReferencedEntity'), x.get('ReferencingEntity')) for x in er]
  # get referenced entities for needed entity
  e = list(filter(lambda x: x[0] == entity_name, re))
  return list(set([x[1] for x in e]))