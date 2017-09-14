# Extract code and name values for CDISC SDTM controlled terminology

## Objective

Extract (CDISC SDTM CT) data from an XML document and output as (semi-colon) delimited text files.

Extended objective: Have SAS import the text files and use them as hash tables to populate codelist-level metadata.


## Input / Source data

[CDISC SDTM controlled terminology in odm-xml format](https://evs.nci.nih.gov/ftp1/CDISC/SDTM/SDTM%20Terminology.odm.xml) < [Parent directory](https://evs.nci.nih.gov/ftp1/CDISC/SDTM/) < [National Cancer Institute (has links to other formats)](https://www.cancer.gov/research/resources/terminology/cdisc)


## Output 

Delimited text files / variables : 

1. codelists.csv /  codelist_code, codelist_description
```
codelist_code;codelist_description 
C115388;6 Minute Walk Test test code.
C115387;6 Minute Walk Test test name.
C101805;Abnormal Involuntary Movement Scale test code.
C101806;Abnormal Involuntary Movement Scale test name.
...
```

2. items.csv / codelist_code, items_code, items_description
```
codelist_code;item_code;item_value
C115388;C115800;SIXMW101
C115388;C115801;SIXMW102
C115388;C115802;SIXMW103
C115388;C115803;SIXMW104
...
```

## Outline / Pseudocode

1. Input/import XML webpage 
2. Extract values from XML 
3. Put values into data frames/sets
4. Output data frames as text files

Python packages used (for step #)
- pandas (3,4)
- re (2)
- urllib (1)
- xml (2)

## Python code

```
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

## initialize namespace dictionary
namespace = {}

## use regular expression to extract default namespace
ns_default = re.findall("{([^}]*)", tree.tag)[0]
#print(ns_default)

## add entries to dictionary
namespace['root.tag'] = tree.tag
namespace['root'] = ns_default
namespace['ct'] = 'http://ncicb.nci.nih.gov/xml/odm/EVS/CDISC'
#print(namespace)

## initialize lists
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
```

## Keywords

Python, xml, regex, pandas,
CDISC, SDTM, metadata, controlled terminology, CT
