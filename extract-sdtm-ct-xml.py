# Noory Kim
# Started 2017-09-08
# Last updated 2017-09-11

# load Python packages into memory
import re
import urllib.request, urllib.parse, urllib.error
import xml.etree.cElementTree as ET

# to assess runtime
from datetime import datetime
start = datetime.now()


# get location of odm-xml file with the controlled terminology
url = input("Enter location: ")
# define default location
if len(url) < 1:
	url = 'https://evs.nci.nih.gov/ftp1/CDISC/SDTM/SDTM%20Terminology.odm.xml'
	
	# url = 'file:///Users/.../Dropbox/2017-training/py4e/SDTM-ct-odm.xml'
print('Retrieving', url)

# open and read file
## xml = urllib.request.urlopen(url, context=ctx).read()
uh = urllib.request.urlopen(url)
data = uh.read()
## print('Retrieved', len(data), 'characters')

# prints xml tree
## print(data.decode())

# use ElementTree package to parse xml
tree = ET.fromstring(data)

# namespace dictionary
namespace = {}

# add entries to dictionary
namespace['root.tag'] = tree.tag
# use regular expression to extract default namespace
ns_default = re.findall("{([^}]*)", tree.tag)[0]
print(ns_default)
namespace['root'] = ns_default
namespace['ct'] = 'http://ncicb.nci.nih.gov/xml/odm/EVS/CDISC'

print(namespace)

# for each CodeList
for codelist in tree.find('root:Study', namespace).find('root:MetaDataVersion', namespace).findall('root:CodeList', namespace):
	codelist_code = codelist.attrib['{http://ncicb.nci.nih.gov/xml/odm/EVS/CDISC}ExtCodeID']
	codelist_description = codelist.find('root:Description', namespace).find('root:TranslatedText', namespace).text
	print("CodeList: ", codelist_code, codelist_description)
	# for each EnumeratedItem in the CodeList
	for item in codelist.findall('root:EnumeratedItem', namespace):
		item_code = item.attrib['{http://ncicb.nci.nih.gov/xml/odm/EVS/CDISC}ExtCodeID']
		item_value = item.attrib['CodedValue']
		print('EnumeratedItem: ', item_code, item_value)

# to assess runtime
print(datetime.now()-start)