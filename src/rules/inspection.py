#!/usr/bin/env python
# * coding: utf8 *
"""
inspection.py
A module that has the UICInspection rules
"""

from config import config
from models.ruletypes import Constant, Constraint
from services.loader import load_rule_for

from . import common

TABLE = "UICInspection"
FOLDER = "inspection"

guid_constant = Constant("Inspection Guid", "GUID", "GUID()")

type_domain_constraint = Constraint(
    "Inspection Type",
    "InspectionType.domain",
    common.constrain_to_domain("InspectionType", allow_null=True, domain="UICInspectionTypeDomain"),
)

type_domain_constraint_update = Constraint(
    "Inspection Type",
    "InspectionType.update",
    common.constrain_to_domain("InspectionType", allow_null=False, domain="UICInspectionTypeDomain"),
)
type_domain_constraint_update.triggers = [config.triggers.update]

assistance_domain_constraint = Constraint(
    "Inspection Assistance",
    "InspectionAssistance",
    common.constrain_to_domain("InspectionAssistance", allow_null=True, domain="UICComplianceAssistanceDomain"),
)

assistance_domain_constraint_update = Constraint(
    "Inspection Assistance",
    "InspectionAssistance",
    common.constrain_to_domain("InspectionAssistance", allow_null=False, domain="UICComplianceAssistanceDomain"),
)
assistance_domain_constraint_update.triggers = [config.triggers.update]

deficiency_domain_constraint = Constraint(
    "Inspection Deficiency",
    "InspectionDeficiency.domain",
    common.constrain_to_domain("InspectionDeficiency", allow_null=True, domain="UICDeficiencyDomain"),
)

deficiency_domain_constraint_update = Constraint(
    "Inspection Deficiency",
    "InspectionDeficiency.update",
    common.constrain_to_domain("InspectionDeficiency", allow_null=False, domain="UICDeficiencyDomain"),
)
deficiency_domain_constraint_update.triggers = [config.triggers.update]

foreign_key_constraint = Constraint("One parent relation", "Single Parent", load_rule_for(FOLDER, "oneFKConstraint"))
foreign_key_constraint.triggers = [config.triggers.update]

facility_only_constraint = Constraint("NW for facility only", "InspectionType", load_rule_for(FOLDER, "typeConstraint"))
facility_only_constraint.triggers = [config.triggers.insert, config.triggers.update]

inspection_date_constraint = Constraint(
    "Well operating status date", "InspectionDate", load_rule_for(FOLDER, "dateConstraint")
)
inspection_date_constraint.triggers = [config.triggers.insert, config.triggers.update]

inspection_date_required_constraint = Constraint(
    "Operating status date", "InspectionDate.Required", common.constrain_to_required("InspectionDate")
)
inspection_date_required_constraint.triggers = [config.triggers.update]

deficiency_constraint = Constraint(
    "No Deficiency", "InspectionDeficiency", load_rule_for(FOLDER, "deficiencyConstraint")
)
deficiency_constraint.triggers = [config.triggers.insert, config.triggers.update]

name_constraint_update = Constraint("Name is required", "Inspector", common.constrain_to_required("Inspector"))
name_constraint_update.triggers = [config.triggers.update]

RULES = [
    guid_constant,
    type_domain_constraint,
    type_domain_constraint_update,
    inspection_date_constraint,
    inspection_date_required_constraint,
    assistance_domain_constraint,
    assistance_domain_constraint_update,
    deficiency_domain_constraint,
    deficiency_domain_constraint_update,
    foreign_key_constraint,
    facility_only_constraint,
    deficiency_constraint,
    name_constraint_update,
]
