#!/usr/bin/env python
# * coding: utf8 *
"""
well.py
A module that holds the rules for uic wells
"""

from . import common
from config import config
from services.loader import load_rule_for
from models.ruletypes import Calculation, Constant, Constraint

TABLE = "UICWell"
FOLDER = "well"

guid_constant = Constant("Well Guid", "GUID", "Guid()")

id_calculation = Calculation("Well Id", "WellId", load_rule_for(FOLDER, "idCalculation"))
id_calculation.triggers = [config.triggers.insert, config.triggers.update]
id_calculation.editable = config.editable.no

well_name_constraint = Constraint("Well Name", "WellName", common.constrain_to_required("WellName"))
well_name_constraint.triggers = [config.triggers.update]

facility_calculation = Calculation("Facility Fk", "Facility_Fk", load_rule_for(FOLDER, "facilityCalculation"))

class_constraint = Constraint(
    "Well Class", "Class", common.constrain_to_domain("WellClass", allow_null=True, domain="UICWellClassDomain")
)

class_constraint_update = Constraint(
    "Well Class", "Class.update", common.constrain_to_domain("WellClass", allow_null=False, domain="UICWellClassDomain")
)
class_constraint_update.triggers = [config.triggers.update]

subclass_constraint = Constraint("Well Subclass", "Subclass", load_rule_for(FOLDER, "subClassConstraint"))
subclass_constraint.triggers = [config.triggers.insert, config.triggers.update]

highpriority_constraint = Constraint("High Priority", "HighPriority", load_rule_for(FOLDER, "highPriorityConstraint"))
highpriority_constraint.triggers = [config.triggers.insert, config.triggers.update]

injection_aquifer_constraint = Constraint(
    "Injection Aquifer Exempt",
    "InjectionAquiferExempt",
    common.constrain_to_domain("InjectionAquiferExempt", allow_null=False, domain="UICYesNoUnknownDomain"),
)
injection_aquifer_constraint.triggers = [config.triggers.insert, config.triggers.update]

no_migration_pet_status_constraint = Constraint(
    "No Migration Pet Status", "NoMigrationPetStatus", load_rule_for(FOLDER, "noMigrationPetStatusConstraint")
)
no_migration_pet_status_constraint.triggers = [config.triggers.insert, config.triggers.update]

facility_type_constraint = Constraint(
    "Class I Facility Type", "ClassIFacilityType", load_rule_for(FOLDER, "facilityTypeConstraint")
)
facility_type_constraint.triggers = [config.triggers.insert, config.triggers.update]

remediation_type_constraint = Constraint(
    "Remediation Project Type", "RemediationProjectType", load_rule_for(FOLDER, "remediationConstraint_insert")
)

remediation_type_constraint_update = Constraint(
    "Remediation Project Type", "RemediationProjectType.update", load_rule_for(FOLDER, "remediationConstraint_update")
)
remediation_type_constraint_update.triggers = [config.triggers.update]

swpz_constraint = Constraint(
    "Well SWPZ", "WellSWPZ", common.constrain_to_domain("WellSWPZ", allow_null=True, domain="UICGWProtectionDomain")
)

swpz_constraint_update = Constraint(
    "Well SWPZ",
    "WellSWPZ.update",
    common.constrain_to_domain("WellSWPZ", allow_null=False, domain="UICGWProtectionDomain"),
)
swpz_constraint_update.triggers = [config.triggers.update]

RULES = [
    guid_constant,
    id_calculation,
    well_name_constraint,
    facility_calculation,
    class_constraint,
    subclass_constraint,
    class_constraint_update,
    highpriority_constraint,
    injection_aquifer_constraint,
    no_migration_pet_status_constraint,
    facility_type_constraint,
    remediation_type_constraint,
    remediation_type_constraint_update,
    swpz_constraint,
    swpz_constraint_update,
]
