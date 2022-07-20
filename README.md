# REDIS FHIR

Prototype implementation of FHIR Resource server, using RedisJSON and RediSearch

## Load Data

The following would load content of the ./data folder into Redis.
```
python load-data.py
```

Tested with the data, generated by Synthea. https://github.com/synthetichealth/synthea

Data is loaded into keys, corresponding to the individual resources.

## Indexing the data

Patient
```
FT.CREATE idx:patient 
  ON JSON
    PREFIX 1 "Patient:"
  SCHEMA
    $.name[0].family AS name_family TEXT SORTABLE
    $.name[0].given[0] AS name_given TEXT SORTABLE
    $.gender AS gender TAG
    $.birthDate AS birthday TEXT SORTABLE
```

Observation
```
FT.CREATE idx:observation  
  ON JSON
    PREFIX 1 "Observation:"
  SCHEMA
    $.subject.reference AS patient TAG
    $.encounter.reference AS encounter TAG
    $.code.coding[0].system AS code_system TAG
    $.code.coding[0].code AS code_code TAG
    $.effectiveDateTime as date_time TEXT SORTABLE
```
Index information
```
FT.INFO "idx:observation"
```
Search for patient with the name starting with `smith`
```
FT.SEARCH idx:patient smith*
```

Search all Observations of type `8302-2` (Body Height) for the patient
`bc9ecb30-dcb0-41cb-b3d6-6b5b30928330` (Micah Smith)
```
FT.SEARCH 'idx:observation' 
  "@patient:{urn\\:uuid\\:bc9ecb30\\-dcb0\\-41cb\\-b3d6\\-6b5b30928330} 
  @code_code:{8302\\-2}" 
  RETURN 2 $.valueQuantity.value $.effectiveDateTime
  SORTBY date_time
```