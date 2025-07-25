## v2.0.0 (2025-07-25)

### Feature

- add ssl args to connection
- add command to test connection
- represent models as dicts
- use script name as log file name
- add a helper method to data models for cleaning dicts
- use convenience function to add user agent header to requests
- add logger
- add session generator function to db utils
- run cli from script
- add cli command to call get_alma_data
- add command to create missing tables for local dev
- add config object using env vars
- add core cli

### Fix

- match cli commands to script names
- add more logging statements
- correctly name gbif_citations table
- use sessionmaker and .begin() to ensure commits
- make columns nullable

### Refactor

- use specific import
- move stats scripts into package
- convert portal_images to use config and sqlalchemy
- convert package_comp to use config and sqlalchemy
- rearrange alma_contents to put main function at the top
- convert gbif_citations to use config and sqlalchemy
- alphabetise gbif_citation fields
- use clearer alias for date
- rename main functions to match script name
- convert dimensions_metrics to use config and sqlalchemy
- move version command into base group
- convert alma_contents to use config and sqlalchemy
- use pyproject.toml and python package
- remove twitter

### Docs

- add basic readme
- inline docs for get-config command

### CI System(s)

- remove patch branch from sync action
- add workflow files
- add pre-commit config

### Chores/Misc

- rename template env file
- remove unused file
- ignore other .env files
- ignore new msq permissions file

## v1.3.1 (2025-07-08)

### Fix

- update error message to contain correct information

## v1.3.0 (2025-07-08)

### Feature

- add SSL connection support for the MySQL database

### Fix

- remove extra bracket accidentally added to portal image entry

### Build System(s)

- add certs directory for ssl db connection

### Chores/Misc

- remove unused import

## v1.2.0 (2025-07-08)

### Feature

- update dependencies and remove secondary dependencies

### Fix

- ensures the script actually works with the updated twitter lib
- update the dependencies again to actually work with python 3.8
- reinstate uncommented sql line (woops)

### Build System(s)

- add a python version file to pin 3.8

### Chores/Misc

- add some other dev paths to gitignore

## v1.1.0 (2025-05-22)

### Fix

- make sure the counts are ints
- use correct key from multi stat response for count
- use the new vds_multi_stat action to get image stats

## v1.0.2 (2021-04-21)

## v1.0.1 (2021-04-15)

## v1.0.0 (2021-04-08)
