#!/usr/bin/env python
# * coding: utf8 *
"""
ruletypes.py
A module that holds the types of rules
"""

from config import config


class BaseType(object):
    def __init__(self):
        self.type = config.rule_types.calculation
        self.editable = config.editable.yes
        self.triggers = config.triggers.insert

        self.description = None
        self.tag = None

        self.arcade = None


class Constant(BaseType):
    def __init__(self, name, field, value):
        super(Constant, self).__init__()

        self.name = name
        self.field = field
        self.rule_name = field
        self.description = name
        self.editable = config.editable.no

        self.arcade = "return {};".format(value)

        self.tag = "Constant"


class Calculation(BaseType):
    def __init__(self, name, field, arcade):
        super(Calculation, self).__init__()

        self.name = name
        self.field = field
        self.rule_name = field
        self.description = name

        self.arcade = arcade

        self.tag = "Calculation"


class Constraint(BaseType):
    def __init__(self, name, rule_name, arcade):
        super(Constraint, self).__init__()

        self.name = name
        self.field = None
        self.rule_name = rule_name
        self.description = name

        self.arcade = arcade

        self.type = config.rule_types.constraint

        self.tag = "Constraint"

        self.error_message = " "
        self.error_number = 112
