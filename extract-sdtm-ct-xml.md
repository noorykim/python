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

[extract-sdtm-ct-xml.py](programs/extract-sdtm-ct-xml.py)


## Keywords

Python, xml, regex, pandas,
CDISC, SDTM, metadata, controlled terminology, CT
