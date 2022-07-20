In this tutorial we will work with FHIR documents

See https://hl7.org/FHIR/ for more information on FHIR

Sample data and load scripts avaliable at https://github.com/antonum/RedisFHIR

## Loading sample data

To load sample data, generated with Synthya - clone the repository and run `load-data.py` script.

```
git clone https://github.com/antonum/RedisFHIR
cd RedisFHIR
python load-data.py
```

## Indexing
```redis Drop indices if exist
FT.DROPINDEX idx:patient
FT.DROPINDEX idx:observation
```

```redis Create indices on Patient and Observation
FT.CREATE idx:patient 
  ON JSON
    PREFIX 1 "Patient:"
  SCHEMA
    $.name[0].family AS name_family TEXT SORTABLE
    $.name[0].given[0] AS name_given TEXT SORTABLE
    $.gender AS gender TAG
    $.birthDate AS birthday TEXT SORTABLE
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
## Searching

List all the patients order by DOB
```redis List Patients
FT.SEARCH idx:patient *  
  RETURN 3 birthday name_family name_given
  SORTBY birthday
```
Search for patient with the name starting with `smith`
```redis Search for Smith*
FT.SEARCH idx:patient smith*
```
Now note the ID of the patient `bc9ecb30-dcb0-41cb-b3d6-6b5b30928330` and search for all Observations of type `8302-2` (Body Height) for that patient
```redis Search for history of specific Observation for Patient
FT.SEARCH 'idx:observation' 
  "@patient:{urn\\:uuid\\:bc9ecb30\\-dcb0\\-41cb\\-b3d6\\-6b5b30928330} 
  @code_code:{8302\\-2}" 
  RETURN 2 $.valueQuantity.value $.effectiveDateTime 
  SORTBY date_time
```