# UIC Attribute Rules

## Setup

1. create local database from sql management studio named `UIC`
1. enable as enterprise gdb via pro

    ```py
    import arcpy
    arcpy.management.EnableEnterpriseGeodatabase(r'...\uic-attribute-rules\pro-project\localhost.sde', r'C:\Program Files\ESRI\License10.6\sysgen\keycodes')
    ```

    _If you receive errors, you may need to execute the following sql_

    ```sql
    ALTER DATABASE UIC
    SET ALLOW_SNAPSHOT_ISOLATION ON

    ALTER DATABASE UIC
    SET READ_COMMITTED_SNAPSHOT ON
    ```

1. import the XML Workspace for the existing UIC database

    ```py
    arcpy.management.ImportXMLWorkspaceDocument(r'...\uic-attribute-rules\pro-project\localhost.sde', r'...\uic-attribute-rules\data\UIC_STAGING.XML', 'SCHEMA_ONLY', None)
    ```

1. Create a python conda workspace for the project

    ```sh
    conda create --clone arcgispro-py3 --name uic
    ```

1. Activate the environment

    ```sh
    activate uic
    ```

1. install the development requirements

    ```sh
    pip install -e .[dev]
    ```

## Installation

### Database Migrations

#### Update Enterprise GDB

1. Update to >= 10.7.1

#### Remove feature dataset

1. Import the individual feature classes contained within the feature datasets
1. Import everything outside the feature dataset
1. Need to transfer the UDEQ.UICADMIN.UICSCHEMATRONERRORCODES by hand (_is this necessary?_)
1. Set the bridging / intermediate table for UICAOR to UICArtPen permissions for all users to Select, Insert, Update, and Delete
   - I think if we grant `data reader` and `data writer` plus `EXECUTE` to all users the above step is unnecessary
1. Database users need to be database authentication for versions to be created correctly.
1. All users besides SDE need to be granted EXECUTE privileges.
1. All users need Select, Insert, Update, and Delete granted via ESRI tools

#### Add reference data

1. County boundaries
1. Municipal boundaries
1. Zip code boundaries

#### python migrations

1. add `localhost.sde`, `stage.sde`, and `prod.sde` to the pro-project
1. run migration code
   - `python migrations.py migrate --env=local, dev, prod`

This is a doc opt cli, so check the help for the tool

##### What happens

1. removes unused tables
1. unversions tables
1. disables editor tracking
1. adds and removes table fields
1. removes unused domains
1. moves fields from one table to another
1. creates well contingency
1. adds editor tracking
1. versions tables

### Attribute Rules

1. add `localhost.sde`, `stage.sde`, and `prod.sde` to the pro-project
1. Install attribute rules
   - `python ar.py update --env=local, dev, prod`
   - You can specify `--rule=` to only update a tables worth of rules

This is a doc opt cli, so check the help for the tool.

## Releasing

1. Bump ar.py `VERSION` string
1. Bump ruletypes.py `Constraint.error_number` to match in the integer form
   - Bump before you run since it adds a record to the `Version_Information` table
1. Bump migration.py if it changed.
   - Bump before you run since it adds a record to the `Version_Information` table
