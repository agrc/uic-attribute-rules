#!/usr/bin/env python
# * coding: utf8 *
"""
enforcement.py
A module that has the UICEnforcement rules
"""

from config import config
from models.ruletypes import Constant, Constraint
from services.loader import load_rule_for

from . import common

TABLE = "UICEnforcement"
FOLDER = "enforcement"

guid_constant = Constant("Enforcement Guid", "GUID", "GUID()")

type_constraint = Constraint(
    "Enforcement Type",
    "EnforcementType",
    common.constrain_to_domain("EnforcementType", allow_null=True, domain="UICEnforcementTypeDomain"),
)

type_constraint_update = Constraint(
    "Enforcement Type",
    "EnforcementType.update",
    common.constrain_to_domain("EnforcementType", allow_null=False, domain="UICEnforcementTypeDomain"),
)
type_constraint_update.triggers = [config.triggers.update]

date_constraint = Constraint("Enforcement Date", "EnforcementDate", load_rule_for(FOLDER, "dateConstraint"))
date_constraint.triggers = [config.triggers.insert, config.triggers.update]

comment_constraint = Constraint("Comment", "Comment", load_rule_for(FOLDER, "commentConstraint"))
comment_constraint.triggers = [config.triggers.insert, config.triggers.update]

RULES = [
    guid_constant,
    type_constraint,
    type_constraint_update,
    date_constraint,
    comment_constraint,
]
