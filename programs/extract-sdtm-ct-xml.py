## Noory Kim
## Started 2017-09-08
## Last updated 2017-09-13

## load Python packages into memory
import re
import urllib.request, urllib.parse, urllib.error
import xml.etree.cElementTree as ET
import pandas as pd

## for calculating runtime at end of program below
from datetime import datetime
start = datetime.now()

## get location of odm-xml file with the controlled terminology
url = input("Enter location: ")
## define default location
if len(url) < 1:
	url = 'https://evs.nci.nih.gov/ftp1/CDISC/SDTM/SDTM%20Terminology.odm.xml'	
	# url = 'file:///Users/.../Dropbox/2017-training/py4e/SDTM-ct-odm.xml'
print('Retrieving', url)

## open and read file
webdata = urllib.request.urlopen(url)
data = webdata.read()

## use ElementTree package to parse xml
tree = ET.fromstring(data)

## setup namespace dictionary
namespace = {}

## use regular expression to extract default namespace
ns_default = re.findall("{([^}]*)", tree.tag)[0]
#print(ns_default)

## add entries to dictionary
namespace['root.tag'] = tree.tag
namespace['root'] = ns_default
namespace['ct'] = 'http://ncicb.nci.nih.gov/xml/odm/EVS/CDISC'
#print(namespace)

## setup lists
codelists = []
items = []

## for each CodeList
for codelist in tree.find('root:Study', namespace).find('root:MetaDataVersion', namespace).findall('root:CodeList', namespace):
	codelist_code = codelist.attrib['{http://ncicb.nci.nih.gov/xml/odm/EVS/CDISC}ExtCodeID']
	codelist_description = codelist.find('root:Description', namespace).find('root:TranslatedText', namespace).text
	#print("CodeList: ", codelist_code, codelist_description)
	codelists.append([codelist_code, codelist_description])

	## for each EnumeratedItem in the CodeList
	for item in codelist.findall('root:EnumeratedItem', namespace):
		item_code = item.attrib['{http://ncicb.nci.nih.gov/xml/odm/EVS/CDISC}ExtCodeID']
		item_value = item.attrib['CodedValue']
		#print('EnumeratedItem: ', item_code, item_value)
		items.append([codelist_code, item_code, item_value])

## output codelists to file
#print(codelists)
codelists_df = pd.DataFrame(codelists)
codelists_df.columns = ['codelist_code', 'codelist_description ']
codelists_df.to_csv('codelists.csv', sep=';', index=False, header=True)
# print(codelists_df)

## output items to file
#print(codelists)
items_df = pd.DataFrame(items)
items_df.columns = ['codelist_code', 'item_code', 'item_value']
items_df.index += 1
items_df.to_csv('items.csv', sep=';', index=False, header=True)
# print(items_df)

## calculate runtime
print('Runtime:', datetime.now()-start)