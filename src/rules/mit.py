#!/usr/bin/env python
# * coding: utf8 *
"""
mit.py
A module that has the UICMIT rules
"""

from config import config
from models.ruletypes import Constant, Constraint
from services.loader import load_rule_for

from . import common

TABLE = "UICMIT"
FOLDER = "mit"

guid_constant = Constant("MIT Guid", "GUID", "GUID()")

type_domain_constraint = Constraint(
    "MIT type", "Type", common.constrain_to_domain("MITType", allow_null=False, domain="UICMITTypeDomain")
)
type_domain_constraint.triggers = [config.triggers.update]

date_constraint_update = Constraint("MIT date", "MITDate.update", common.constrain_to_required("MITDate"))
date_constraint_update.triggers = [config.triggers.update]

result_constraint_update = Constraint("MIT result", "MITResult.update", common.constrain_to_required("MITResult"))
result_constraint_update.triggers = [config.triggers.update]

type_constraint = Constraint("MIT Date and Type", "MITDate", load_rule_for(FOLDER, "typeConstraint"))
type_constraint.triggers = [config.triggers.insert, config.triggers.update]

result_constraint = Constraint("MIT Result and Type", "MITResult", load_rule_for(FOLDER, "resultConstraint"))
result_constraint.triggers = [config.triggers.insert, config.triggers.update]

remediation_constraint = Constraint(
    "MIT Remediation Action and Result", "RemediationAction", load_rule_for(FOLDER, "remediationConstraint")
)
remediation_constraint.triggers = [config.triggers.insert, config.triggers.update]

remediation_date_constraint = Constraint(
    "Remediation Action Date and Remediation Action", "RemActDate", load_rule_for(FOLDER, "remediationDate")
)
remediation_date_constraint.triggers = [config.triggers.update]

comment_constraint = Constraint("Comment for Other Action", "Comment", load_rule_for(FOLDER, "commentConstraint"))
comment_constraint.triggers = [config.triggers.insert, config.triggers.update]

comment_mittype_constraint = Constraint(
    "Comment for MIT Type", "Comment.MITType", load_rule_for(FOLDER, "commentMitTypeConstraint")
)
comment_mittype_constraint.triggers = [config.triggers.insert, config.triggers.update]

mit_rem_date_constraint = Constraint("Rem ACT date", "MITRemActDate", load_rule_for(FOLDER, "dateConstraint"))
mit_rem_date_constraint.triggers = [config.triggers.update]

RULES = [
    guid_constant,
    type_domain_constraint,
    date_constraint_update,
    result_constraint_update,
    type_constraint,
    result_constraint,
    remediation_constraint,
    remediation_date_constraint,
    comment_constraint,
    comment_mittype_constraint,
    mit_rem_date_constraint,
]
