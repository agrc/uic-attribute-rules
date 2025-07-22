#!/usr/bin/env python
# * coding: utf8 *
"""
ar

Usage:
    ar update [--rule=<rule> --env=<env>]
    ar delete [--rule=<rule> --env=<env>]
    ar --version
    ar (-h | --help)

Options:
    --rule=<rule>   The allowable rules.
                        area_of_review, art_pen, authorization, authorization_action, contact, correction, enforcement, facility, inspection, mit,
                        operating_status, violation, well, ALL
    --env=<env>     local, dev, prod
    -h --help       Shows this screen
    -v --version    Shows the version
"""

import os
from datetime import datetime

import arcpy
from arcgisscripting import ExecuteError  # pylint: disable=no-name-in-module
from docopt import docopt

from config.config import get_sde_path_for
from models.rule import RuleGroup
from rules import (
    area_of_review,
    art_pen,
    authorization,
    authorization_action,
    contact,
    correction,
    enforcement,
    facility,
    inspection,
    mit,
    operating_status,
    violation,
    well,
)

VERSION = "1.2.1"


def get_rules(sde, rule=None):
    if rule == "ALL":
        tables = [
            facility.TABLE,
            well.TABLE,
            area_of_review.TABLE,
            art_pen.TABLE,
            authorization.TABLE,
            authorization_action.TABLE,
            contact.TABLE,
            correction.TABLE,
            enforcement.TABLE,
            inspection.TABLE,
            mit.TABLE,
            operating_status.TABLE,
            violation.TABLE,
        ]

        for table in tables:
            attribute_rules = arcpy.Describe(os.path.join(sde, table)).attributeRules

            calculation_rules = ";".join([ar.name for ar in attribute_rules if "Calculation" in ar.type])
            constraint_rules = ";".join([ar.name for ar in attribute_rules if "Constraint" in ar.type])

            if calculation_rules:
                print("  deleting calculation rules: {}".format(calculation_rules))
                try:
                    arcpy.management.DeleteAttributeRule(
                        in_table=os.path.join(sde, table),
                        names=calculation_rules,
                        type="CALCULATION",
                    )
                    print("    deleted")
                except ExecuteError as e:
                    (message,) = e.args

                    if message.startswith("ERROR 002556"):
                        print("    rule already deleted, skipping...")
                    else:
                        raise e

            if constraint_rules:
                print("  deleting constraint rules {}".format(constraint_rules))
                try:
                    arcpy.management.DeleteAttributeRule(
                        in_table=os.path.join(sde, table),
                        names=constraint_rules,
                        type="CONSTRAINT",
                    )
                    print("    deleted")
                except ExecuteError as e:
                    (message,) = e.args

                    if message.startswith("ERROR 002556"):
                        print("    rule already deleted, skipping...")
                    else:
                        raise e

        return []

    facility_rules = RuleGroup(sde, facility.TABLE, facility.RULES)
    well_rules = RuleGroup(sde, well.TABLE, well.RULES)
    aor_rules = RuleGroup(sde, area_of_review.TABLE, area_of_review.RULES)
    art_pen_rules = RuleGroup(sde, art_pen.TABLE, art_pen.RULES)
    authorization_rules = RuleGroup(sde, authorization.TABLE, authorization.RULES)
    auth_action_rules = RuleGroup(sde, authorization_action.TABLE, authorization_action.RULES)
    contact_rules = RuleGroup(sde, contact.TABLE, contact.RULES)
    correction_rules = RuleGroup(sde, correction.TABLE, correction.RULES)
    enforcement_rules = RuleGroup(sde, enforcement.TABLE, enforcement.RULES)
    inspection_rules = RuleGroup(sde, inspection.TABLE, inspection.RULES)
    mit_rules = RuleGroup(sde, mit.TABLE, mit.RULES)
    operating_status_rules = RuleGroup(sde, operating_status.TABLE, operating_status.RULES)
    violation_rules = RuleGroup(sde, violation.TABLE, violation.RULES)

    if rule is None:
        return [
            facility_rules,
            well_rules,
            aor_rules,
            art_pen_rules,
            auth_action_rules,
            authorization_rules,
            contact_rules,
            correction_rules,
            enforcement_rules,
            inspection_rules,
            mit_rules,
            operating_status_rules,
            violation_rules,
        ]

    rules = {
        "area_of_review": aor_rules,
        "art_pen": art_pen_rules,
        "authorization": authorization_rules,
        "authorization_action": auth_action_rules,
        "contact": contact_rules,
        "correction": correction_rules,
        "enforcement": enforcement_rules,
        "facility": facility_rules,
        "inspection": inspection_rules,
        "mit": mit_rules,
        "operating_status": operating_status_rules,
        "violation": violation_rules,
        "well": well_rules,
    }

    return [rules[rule]]


def update_version(sde, version):
    with arcpy.da.InsertCursor(
        in_table=os.path.join(sde, "Version_Information"), field_names=["name", "version", "date"]
    ) as cursor:
        date = datetime.datetime.now()
        date_string = str(date).split(" ")[0]
        cursor.insertRow(("attribute rules", version, date_string))


def main():
    """Main entry point for program. Parse arguments and pass to engine module"""
    args = docopt(__doc__, version=VERSION)

    sde = get_sde_path_for(args["--env"])
    print("acting on {}".format(sde))

    if not arcpy.TestSchemaLock(os.path.join(sde, facility.TABLE)):
        print("Unable to reach the database or acquire the necessary schema lock to add rules")
        exit(0)

    if args["update"]:
        for rule in get_rules(sde, args["--rule"]):
            rule.execute()

        update_version(sde, VERSION)
    elif args["delete"]:
        for rule in get_rules(sde, args["--rule"]):
            rule.delete()

    arcpy.management.ClearWorkspaceCache(sde)


if __name__ == "__main__":
    main()
