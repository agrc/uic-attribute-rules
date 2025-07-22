#!/usr/bin/env python
# * coding: utf8 *
"""
authorization.py
A module that has the UICAuthorization rules
"""

from config import config
from models.ruletypes import Calculation, Constant, Constraint
from services.loader import load_rule_for

from . import common

TABLE = "UICAuthorization"
FOLDER = "authorization"

guid_constant = Constant("Authorization Guid", "GUID", "GUID()")

id_calculation = Calculation("Authorization Id", "AuthorizationID", load_rule_for(FOLDER, "idCalculation"))
id_calculation.triggers = [config.triggers.insert, config.triggers.update]
id_calculation.editable = config.editable.no

start_date_constraint_update = Constraint("Start Date", "StartDate.update", common.constrain_to_required("startdate"))
start_date_constraint_update.triggers = [config.triggers.update]

type_domain_constraint = Constraint(
    "Authorization Type",
    "AuthorizationType",
    common.constrain_to_domain("AuthorizationType", allow_null=True, domain="UICAuthorizeTypeDomain"),
)

type_domain_constraint_update = Constraint(
    "Authorization Type",
    "AuthorizationType.update",
    common.constrain_to_domain("AuthorizationType", allow_null=False, domain="UICAuthorizeTypeDomain"),
)
type_domain_constraint_update.triggers = [config.triggers.update]

type_constraint = Constraint(
    "Authorization Type Default", "AuthorizationTypeDefault", load_rule_for(FOLDER, "authorizationTypeConstraint")
)
type_constraint.triggers = [config.triggers.update]

sector_type_constraint = Constraint(
    "Owner Sector Type",
    "OwnerSectorType",
    common.constrain_to_domain("OwnerSectorType", allow_null=True, domain="UICOwnerSectorTypeDomain"),
)

sector_type_constraint_update = Constraint(
    "Owner Sector Type",
    "OwnerSectorType.update",
    common.constrain_to_domain("OwnerSectorType", allow_null=False, domain="UICOwnerSectorTypeDomain"),
)
sector_type_constraint_update.triggers = [config.triggers.update]

RULES = [
    guid_constant,
    id_calculation,
    type_domain_constraint,
    type_domain_constraint_update,
    type_constraint,
    start_date_constraint_update,
    sector_type_constraint,
    sector_type_constraint_update,
]
