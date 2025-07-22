#!/usr/bin/env python
# * coding: utf8 *
"""
art_pen.py
A module that has the UICArtPen rules
"""

from config import config
from models.ruletypes import Constant, Constraint
from services.loader import load_rule_for

from . import common

TABLE = "UICArtPen"
FOLDER = "artPen"

guid_constraint = Constant("Art Pen Guid", "GUID", "GUID()")

name_constraint = Constraint("Art Pen Well Name", "ArtPen_WellName", common.constrain_to_required("ArtPen_WellName"))
name_constraint.triggers = [config.triggers.update]

well_type_constraint = Constraint(
    "Art Pen Well Type",
    "ArtPen_WellType",
    common.constrain_to_domain("ArtPen_WellType", allow_null=True, domain="UICArtPenWellType"),
)

well_type_constraint_update = Constraint(
    "Art Pen Well Type",
    "ArtPen_WellType.update",
    common.constrain_to_domain("ArtPen_WellType", allow_null=False, domain="UICArtPenWellType"),
)
well_type_constraint_update.triggers = [config.triggers.update]

review_date_constraint = Constraint(
    "Art Pen Review Date", "Artpen_ReviewDate", load_rule_for(FOLDER, "reviewDateConstraint")
)
review_date_constraint.triggers = [config.triggers.insert, config.triggers.update]

catype_constraint = Constraint("Art Pen Review Date", "ArtPen_CAType", load_rule_for(FOLDER, "caTypeConstraint"))
catype_constraint.triggers = [config.triggers.insert, config.triggers.update]

cadate_constraint = Constraint("CA Date", "ArtPen_CADate", load_rule_for(FOLDER, "caDateConstraint"))
cadate_constraint.triggers = [config.triggers.insert, config.triggers.update]

comment_constraint = Constraint("Art Pen Other Ca", "Comments", load_rule_for(FOLDER, "commentConstraint"))
comment_constraint.triggers = [config.triggers.update]

RULES = [
    guid_constraint,
    name_constraint,
    well_type_constraint,
    well_type_constraint_update,
    review_date_constraint,
    catype_constraint,
    cadate_constraint,
    comment_constraint,
]
