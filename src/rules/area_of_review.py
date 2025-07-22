#!/usr/bin/env python
# * coding: utf8 *
"""
area_of_review.py
A module that has the UICAreaOfReview rules
"""

from models.ruletypes import Constant

TABLE = "UICAreaOfReview"

guid_constant = Constant("Area Of Review Guid", "GUID", "GUID()")

RULES = [guid_constant]
