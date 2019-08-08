#!/usr/bin/env python
# * coding: utf8 *
'''
migrations

Usage:
    migrations migrate [--env=<env>]
    migrations --version
    migrations (-h | --help)

Options:
    --env=<env>     local, dev, prod
    -h --help       Shows this screen
    -v --version    Shows the version
'''

import os

from arcgisscripting import ExecuteError  # pylint: disable=no-name-in-module
from docopt import docopt

import arcpy
from config import config

_tables_to_delete = [
    'UICAlternateDisposal',
    'UICAquiferRemediation',
    'UICBMPElement',
    'UICClassIConstituent',
    'UICClassIWaste',
    'UICConstructionElement',
    'UICDeepWellOperation',
    'UICVerticalWellEvent',
    'DEQFacilities',
    'UICSCHEMATRONERRORCODES',
    'UICToolbox',
]
_skip_tables = [
    'Counties',
    'ZipCodes',
    'Municipalities',
    'SDE_compress_log',
    'Version_Information',
]
_table_modifications = {
    'UICFacility': {
        'add': [],
        'delete': ['FRSID', 'FacilityState']
    },
    'UICWell': {
        'add': [{
            'in_table': 'UICWell',
            'field_name': 'WellDepth',
            'field_type': 'LONG',
            'field_length': '#',
            'field_precision': 10,
            'field_scale': 0,
            'field_alias': 'Well Depth in Feet',
            'field_is_nullable': 'NULLABLE'
        }],
        'delete': ['ConvertedOGWell', 'LocationMethod', 'LocationAccuracy']
    },
    'UICInspection': {
        'add': [],
        'delete': ['ICISCompMonActReason', 'ICISCompMonType', 'ICISCompActType', 'ICISMOAPriority', 'ICISRegionalPriority']
    },
    'UICContact': {
        'add': [],
        'delete': ['ContactFax']
    },
    'UICArtPen': {
        'add': [
            {
                'in_table': 'UICArtPen',
                'field_name': 'EditedBy',
                'field_type': 'TEXT',
                'field_length': 40,
                'field_precision': '#',
                'field_scale': '#',
                'field_alias': 'EditedBy',
                'field_is_nullable': 'NULLABLE'
            },
            {
                'in_table': 'UICArtPen',
                'field_name': 'ArtPenWellDepth',
                'field_type': 'LONG',
                'field_length': '#',
                'field_precision': 10,
                'field_scale': 0,
                'field_alias': 'ArtPenWellDepth',
                'field_is_nullable': 'NULLABLE'
            },
        ],
        'delete': ['EditedBy']
    }
}
_domains_to_delete = [
    'UICAlternateDisposalTypeDomain',
    'UICAquiferRemediationDomain',
    'UICBMPElementTypeDomain',
    'UICConcentrationUnitDomain',
    'UICConstructionElementTypeDomain',
    'UICEventTypeDomain',
    'UICEventUnitsDomain',
    'UICCityDomain',
    'UICZoningCategoryDomain',
    'UICLocationMethodDomain',
    'UICLocationalAccuracyDomain',
    'UICICISCompActTypeDomain',
    'UICICISCompMonActReasonDomain',
    'UICICISMonitoringTypeDomain',
]
_domains_to_update = {
    'UICArtPenCAType': {
        'code': '5',
        'value': 'waiting'
    },
    'UICNoMigrationPetStatusDomain': {
        'code': 'WA',
        'value': 'waiting'
    },
    'UICMITRemediationActionDomain': {
        'code': 'WA',
        'value': 'waiting'
    }
}


def clean_up(sde):
    print('compressing db')

    try:
        arcpy.management.Compress(sde)
    except Exception:
        print('skipping compress, insufficient permissions')

    print('analyzing db')
    try:
        arcpy.management.AnalyzeDatasets(
            input_database=sde,
            include_system='SYSTEM',
            analyze_base='ANALYZE_BASE',
            analyze_delta='ANALYZE_DELTA',
            analyze_archive='ANALYZE_ARCHIVE',
        )
    except Exception:
        print('skipping analyze, insufficient permissions')


def delete_tables(tables, sde):
    print('removing {} tables'.format(len(tables)))

    for table in tables:
        arcpy.management.Delete(os.path.join(sde, table))

    print('done')


def version_tables(version, tables, skip_tables, sde):
    for table_name in tables:
        parts = table_name.split('.')
        if parts[2] in skip_tables:
            continue

        if version:
            print('updating editor tracking and versioning for {} tables'.format(len(tables) - len(skip_tables)))
            print('  ' + table_name)
            arcpy.management.EnableEditorTracking(
                in_dataset=os.path.join(sde, table_name),
                creator_field='CreatedBy',
                creation_date_field='CreatedOn',
                last_editor_field='EditedBy',
                last_edit_date_field='ModifiedOn',
                add_fields='ADD_FIELDS',
                # record_dates_in='UTC',
            )

            arcpy.management.RegisterAsVersioned(
                in_dataset=os.path.join(sde, table_name),
                edit_to_base='NO_EDITS_TO_BASE',
            )
        else:
            print('unversioning {} tables'.format(len(tables) - len(skip_tables)))
            print('  ' + table_name)
            arcpy.management.UnregisterAsVersioned(
                in_dataset=os.path.join(sde, table_name),
                keep_edit='NO_KEEP_EDIT',
            )

            arcpy.management.DisableEditorTracking(
                in_dataset=os.path.join(sde, table_name),
                creator='DISABLE_CREATOR',
                creation_date='DISABLE_CREATION_DATE',
                last_editor='DISABLE_LAST_EDITOR',
                last_edit_date='DISABLE_LAST_EDIT_DATE',
            )

    print('done')


def modify_tables(changes, sde):
    print('applying table modifications')
    for table_name in changes:
        modifications = changes[table_name]

        deletes = modifications['delete']
        adds = modifications['add']

        try:
            if deletes:
                arcpy.management.DeleteField(os.path.join(sde, table_name), deletes)

            for add in adds:
                arcpy.management.AddField(
                    in_table=os.path.join(sde, add['in_table']),
                    field_name=add['field_name'],
                    field_type=add['field_type'],
                    field_precision=add['field_precision'],
                    field_scale=add['field_scale'],
                    field_length=add['field_length'],
                    field_alias=add['field_alias'],
                    field_is_nullable=add['field_is_nullable']
                )
        except ExecuteError as e:
            message, = e.args

            if 'ERROR 002557' in message:
                print('  field likely upgraded already')
            else:
                print(e)
    print('done')


def delete_domains(domains, sde):
    print('removing {} domains'.format(len(domains)))

    for domain in domains:
        try:
            arcpy.management.DeleteDomain(sde, domain)
        except ExecuteError as e:
            message, = e.args

            if 'ERROR 000800' in message:
                print('  domain already removed')
            else:
                print(e)

    print('done')


def migrate_fields():
    print('moving fields')
    move_field = 'NoMigrationPetStatus'
    from_table = 'UICFacility'
    to_table = 'UICWell'

    migration_pet_status = False
    if len(arcpy.ListFields(from_table, move_field)) == 0:
        migration_pet_status = True
        print('  migration likely completed')

    if not migration_pet_status:
        if len(arcpy.ListFields(to_table, move_field)) < 1:
            arcpy.management.AddField(
                in_table=to_table,
                field_name=move_field,
                field_type='TEXT',
                field_alias=move_field,
                field_domain='UICNoMigrationPetStatusDomain',
                field_is_nullable='NULLABLE',
                field_length=2,
            )

            arcpy.management.AssignDefaultToField(in_table=to_table, field_name=move_field, default_value='NA')

        print('building data cache')
        status_cache = {}
        with arcpy.da.SearchCursor(in_table=from_table, field_names=['GUID', move_field], where_clause='1=1') as cursor:
            for pk, status in cursor:
                status_cache[pk] = status
        print('done')

        print('updating new field data')
        ok = True
        with arcpy.da.UpdateCursor(in_table=to_table, field_names=['Facility_FK', move_field]) as cursor:
            for fk, _ in cursor:
                if fk not in status_cache:
                    continue

                try:
                    cursor.updateRow((fk, status_cache[fk]))
                except Exception as e:
                    ok = False
                    print('update failed ' + str(e))
        print('done')

        if ok:
            print('removing field')
            arcpy.management.DeleteField(from_table, move_field)

    move_field = 'FacilityType'
    new_name = 'ClassIFacilityType'

    facility_type = False
    if len(arcpy.ListFields(from_table, move_field)) < 1:
        facility_type = True
        print('  migration likely completed')

    if not facility_type:
        if len(arcpy.ListFields(to_table, new_name)) < 1:
            arcpy.management.AddField(
                in_table=to_table,
                field_name=new_name,
                field_type='TEXT',
                field_alias='Facility Type for Class I Wells',
                field_domain='UICFacilityTypeDomain',
                field_is_nullable='NULLABLE',
                field_length=1,
            )

            arcpy.management.AssignDefaultToField(in_table=to_table, field_name=new_name)

        print('building data cache')
        type_cache = {}
        with arcpy.da.SearchCursor(in_table=from_table, field_names=['GUID', move_field], where_clause='1=1') as cursor:
            for pk, status in cursor:
                type_cache[pk] = status
        print('done')

        print('updating new field data')
        ok = True
        with arcpy.da.UpdateCursor(in_table=to_table, field_names=['Facility_FK', new_name]) as cursor:
            for fk, _ in cursor:
                if fk not in type_cache:
                    continue

                try:
                    cursor.updateRow((fk, type_cache[fk]))
                except Exception as e:
                    ok = False
                    print('update failed ' + str(e))
        print('done')

        if ok:
            print('removing field')
            arcpy.management.DeleteField(from_table, move_field)


def create_contingencies(sde):
    print('creating contingent field group for well class')

    try:
        arcpy.management.DeleteFieldGroup(
            target_table='UICWell',
            name='Well Class',
        )
    except ExecuteError as e:
        message, = e.args

        if 'ERROR 002585' in message:
            pass
        else:
            print(e)

    try:
        arcpy.management.CreateFieldGroup(
            target_table='UICWell',
            name='Well Class',
            fields=['WellClass', 'WellSubclass'],
        )
    except ExecuteError as e:
        print(e)
    print('done')

    domains = arcpy.da.ListDomains(sde)
    well_subclass = [x for x in domains if x.name == 'UICWellSubClassDomain'][0].codedValues

    print('adding well class contingent values')
    arcpy.management.AddContingentValue(
        target_table='UICWell',
        field_group_name='Well Class',
        values=[['WellClass', 'ANY'], ['WellSubclass', 'NULL']],
    )

    codes = []
    for code, _ in well_subclass.items():
        well_class = int(str(code)[:1])

        if well_class == 7:
            continue

        codes.append((well_class, code))

    codes.sort(key=lambda x: x[1])

    for well_class, code in codes:
        arcpy.management.AddContingentValue(
            target_table='UICWell',
            field_group_name='Well Class',
            values=[['WellClass', 'CODED_VALUE', well_class], ['WellSubclass', 'CODED_VALUE', code]],
        )
    print('done')


def alter_domains(changes, sde):
    for domain_name in changes:
        modification = changes[domain_name]

        try:
            arcpy.management.AddCodedValueToDomain(sde, domain_name, modification['code'], modification['value'])
        except Exception:
            print('  domain probably already added')


def _get_tables(sde):
    tables = arcpy.ListFeatureClasses() + arcpy.ListTables()

    for dataset in arcpy.ListDatasets('', 'Feature'):
        arcpy.env.workspace = os.path.join(sde, dataset)
        tables += arcpy.ListFeatureClasses()

    return tables


if __name__ == '__main__':
    '''Main entry point for program. Parse arguments and pass to engine module
    '''
    args = docopt(__doc__, version='1.0.0')

    arcpy.env.workspace = sde = config.get_sde_path_for(args['--env'])

    print('acting on {}'.format(sde))

    if args['migrate']:
        clean_up(sde)

        delete_tables(_tables_to_delete, sde)

        tables = _get_tables(sde)

        version_tables(False, tables, _skip_tables, sde)
        modify_tables(_table_modifications, sde)
        delete_domains(_domains_to_delete, sde)
        migrate_fields()
        create_contingencies(sde)
        alter_domains(_domains_to_update, sde)
        version_tables(True, tables, _skip_tables, sde)
