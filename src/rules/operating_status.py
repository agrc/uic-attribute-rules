#!/usr/bin/env python
# * coding: utf8 *
"""
operating_status.py
A module that has the UICWellOperatingStatus rules
"""

from config import config
from models.ruletypes import Constant, Constraint
from services.loader import load_rule_for

from . import common

TABLE = "UICWellOperatingStatus"
FOLDER = "operatingStatus"

guid_constant = Constant("Well operating status Guid", "GUID", "GUID()")

type_domain_constraint = Constraint(
    "Operating Status Type",
    "OperatingStatusType",
    common.constrain_to_domain("OperatingStatusType", allow_null=False, domain="UICOperatingStatusTypeDomain"),
)
type_domain_constraint.triggers = [config.triggers.update]

date_constraint = Constraint("Operating Status Date", "OperatingStatusDate", load_rule_for(FOLDER, "dateConstraint"))
date_constraint.triggers = [config.triggers.insert, config.triggers.update]

type_constraint = Constraint(
    "Operating status type needs a date",
    "OperatingStatusType date requirement",
    load_rule_for(FOLDER, "typeConstraint"),
)
type_constraint.triggers = [config.triggers.insert, config.triggers.update]

RULES = [
    guid_constant,
    type_domain_constraint,
    date_constraint,
    type_constraint,
]
