#!/usr/bin/env python
# * coding: utf8 *
"""
authorization_action.py
A module that has the UICAuthorizationAction rules
"""

from config import config
from models.ruletypes import Constant, Constraint
from services.loader import load_rule_for

from . import common

TABLE = "UICAuthorizationAction"
FOLDER = "authorizationAction"

guid_constant = Constant("Authorization Action Guid", "GUID", "GUID()")

action_type_domain_constraint = Constraint(
    "Authorization Action Type",
    "AuthorizationActionType",
    common.constrain_to_domain("AuthorizationActionType", allow_null=True, domain="UICAuthorizeActionTypeDomain"),
)

action_type_domain_constraint_update = Constraint(
    "Authorization Action Type",
    "AuthorizationActionType.update",
    common.constrain_to_domain("AuthorizationActionType", allow_null=False, domain="UICAuthorizeActionTypeDomain"),
)
action_type_domain_constraint_update.triggers = [config.triggers.update]

action_date_constraint = Constraint(
    "Authorization Action Date",
    "AuthorizationActionDate and AuthorizationActionType",
    load_rule_for(FOLDER, "dateConstraint"),
)
action_date_constraint.triggers = [config.triggers.insert, config.triggers.update]

action_type_constraint = Constraint(
    "Authorization Action Type",
    "AuthorizationActionType and AuthorizationActionDate",
    load_rule_for(FOLDER, "typeConstraint"),
)
action_type_constraint.triggers = [config.triggers.insert, config.triggers.update]

RULES = [
    guid_constant,
    action_type_domain_constraint,
    action_type_domain_constraint_update,
    action_date_constraint,
    action_type_constraint,
]
