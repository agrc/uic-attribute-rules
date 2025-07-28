#!/usr/bin/env python
# * coding: utf8 *
"""
contact.py
A module that has the UICContact rules
"""

from config import config
from models.ruletypes import Constant, Constraint
from services.loader import load_rule_for

from . import common

TABLE = "UICContact"
FOLDER = "contact"

guid_constant = Constant("Contact Guid", "GUID", "GUID()")

name_constraint_update = Constraint("Contact Name", "ContactName.update", common.constrain_to_required("ContactName"))
name_constraint_update.triggers = [config.triggers.update]

phone_constraint_update = Constraint(
    "Contact phone", "ContactPhone.update", common.constrain_to_required("ContactPhone")
)
phone_constraint_update.triggers = [config.triggers.update]

organization_constraint_update = Constraint(
    "Contact Organization", "ContactOrganization.update", common.constrain_to_required("ContactOrganization")
)
organization_constraint_update.triggers = [config.triggers.update]

address_constraint_update = Constraint(
    "Contact mailing address", "ContactMailAddress.update", common.constrain_to_required("ContactMailAddress")
)
address_constraint_update.triggers = [config.triggers.update]

city_constraint_update = Constraint(
    "Contact mailing city", "ContactMailCity.update", common.constrain_to_required("ContactMailCity")
)
city_constraint_update.triggers = [config.triggers.update]

state_constraint = Constraint(
    "Contact Mail State",
    "ContactMailState",
    common.constrain_to_domain("ContactMailState", allow_null=True, domain="UICStateDomain"),
)

state_constraint_update = Constraint(
    "Contact Mail State",
    "ContactMailState.update",
    common.constrain_to_domain("ContactMailState", allow_null=False, domain="UICStateDomain"),
)
state_constraint_update.triggers = [config.triggers.update]

type_constraint = Constraint(
    "Contact Type",
    "ContactType",
    common.constrain_to_domain("ContactType", allow_null=True, domain="UICContactTypeDomain"),
)

type_constraint_update = Constraint(
    "Contact Type",
    "ContactType.update",
    common.constrain_to_domain("ContactType", allow_null=False, domain="UICContactTypeDomain"),
)
type_constraint_update.triggers = [config.triggers.update]

contact_type_constraint = Constraint("Owner Operator", "OwnerType", load_rule_for(FOLDER, "contactType"))
contact_type_constraint.triggers = [config.triggers.update]

RULES = [
    guid_constant,
    type_constraint,
    state_constraint,
    contact_type_constraint,
    type_constraint_update,
    name_constraint_update,
    organization_constraint_update,
    address_constraint_update,
    phone_constraint_update,
    city_constraint_update,
    state_constraint_update,
    state_constraint,
]
