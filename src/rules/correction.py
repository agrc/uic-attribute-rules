#!/usr/bin/env python
# * coding: utf8 *
"""
correction.py
A module that has the UICCorrection rules
"""

from config import config
from models.ruletypes import Constant, Constraint
from services.loader import load_rule_for

from . import common

TABLE = "UICCorrection"
FOLDER = "correction"

guid_constant = Constant("Correction Guid", "GUID", "GUID()")

type_constraint = Constraint(
    "Corrective Action",
    "CorrectiveAction",
    common.constrain_to_domain("CorrectiveAction", allow_null=True, domain="UICCorrectiveActionDomain"),
)

type_constraint_update = Constraint(
    "Corrective Action",
    "CorrectiveAction.update",
    common.constrain_to_domain("CorrectiveAction", allow_null=False, domain="UICCorrectiveActionDomain"),
)
type_constraint_update.triggers = [config.triggers.update]

comment_constraint = Constraint("Comment", "Comment", load_rule_for(FOLDER, "commentConstraint"))
comment_constraint.triggers = [config.triggers.insert, config.triggers.update]

RULES = [
    guid_constant,
    type_constraint,
    comment_constraint,
    type_constraint_update,
]
