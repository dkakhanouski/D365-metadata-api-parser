import xml.etree.ElementTree
from functools import reduce
from pprint import pprint as pp
from ODataRelationshipDefinitionsParser import get_referenced_entities as re

# generate sql 'CREATE TABLE' statement from entity
def create_sql(entity):
  pk = ''
  fields = ''
  if entity['Key']:
    pk = '  ' +\
         entity['Key'].find('{http://docs.oasis-open.org/odata/ns/edm}PropertyRef').get('Name') +\
         ' STRING PRIMARY_KEY,\n'
  if entity['Properties']:
    for prop in entity['Properties']:
      if prop.get('Type') in ('Edm.Int32', 'Edm.Int64'):
        fields += '  ' + prop.get('Name') + ' INT,\n'
      elif prop.get('Type') in ('Edm.Decimal', 'Edm.Double'):
        fields += '  ' + prop.get('Name') + ' DOUBLE,\n'
      else:
        fields += '  ' + prop.get('Name') + ' STRING,\n'
  sql_columns = (pk + fields)[:-2]
  return 'CREATE TABLE ' + entity['Name'] + ' (\n' + sql_columns + '\n);\n'

# get xml tags with entities
e = xml.etree.ElementTree.parse('ODataV4Metadata.xml').getroot()\
    .find('{http://docs.oasis-open.org/odata/ns/edmx}DataServices')\
    .find('{http://docs.oasis-open.org/odata/ns/edm}Schema')\
    .findall('{http://docs.oasis-open.org/odata/ns/edm}EntityType')
print(len(e))
# get entities
a = list(map(lambda x: {'Name': x.get('Name'),\
                         'Key': x.find('{http://docs.oasis-open.org/odata/ns/edm}Key'),\
                  'Properties': x.findall('{http://docs.oasis-open.org/odata/ns/edm}Property')}, e))
# remove internal entities
a = list(filter(lambda x: 'Metadata' not in x['Name'] and\
                        'crmmodelbaseentity' not in x['Name'] and\
                        'crmbaseentity' not in x['Name'], a))

# for item in a:
#   print(item['Name'])

# create sql
s = {x['Name']: create_sql(x) for x in a}
# print(s['account'] +\
#       s['activitypointer'] +\
#       s['invoice'] +\
#       s['invoicedetail']+\
#       s['opportunity'] +\
#       s['psa_project'] +\
#       s['psa_projectstatus'] +\
#       s['psa_psauser'], file=open("C:\\Users\\dkakhanouski\\Documents\\output.txt", "a"))

retrievedentities = s.keys()
reportentities = ['account', 'activitypointer', 'invoice', 'invoicedetail',\
                'opportunity', 'psa_project', 'psa_projectstatus', 'psa_psauser']
for entity in reportentities:
  refedsql = ''
  refedentities = re(entity)
  print(entity + ' ' + str(len(refedentities)))
  for bind in refedentities:
    if bind in retrievedentities:
      refedsql += s[bind]
    else:
      print(entity + ' ' + bind)
  #print(refedsql, file=open("C:\\Users\\dkakhanouski\\Documents\\" + entity + "_relations.txt", "a"))

# # pp(re('account'))
#   temp = re(entity)
#   # print(s[temp[0]])
#   for bind in temp:
#     None
#     # print(bind)
# # print(s['lead'])
# print(s.keys())

# for item in a:
#   if item['Key']:
#     print(item['Key'].find('{http://docs.oasis-open.org/odata/ns/edm}PropertyRef').get('Name'))

# for item in a:
#   for j in item['Properties']:
#     if j.get('Type') in ('Edm.Int32', 'Edm.Int64'):
#       print(j.get('Name') + ' INT')
#     elif j.get('Type') in ('Edm.Decimal', 'Edm.Double'):
#       print(j.get('Name') + ' DOUBLE')
#     else:
#       print(j.get('Name') + ' STRING')

# Property types
# t = set(reduce(lambda x, y: x + y, list(map(lambda x: list(map(lambda y: y.get('Type'), x['Properties'])),a))))
# pp(t)
