#!/usr/bin/env python
# * coding: utf8 *
"""
loader.py
A module that loads js arcade scripts into text
"""

import os

ARCADE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "rules", "arcade")


def load_rule_for(rule_type, name):
    rule_location = os.path.join(ARCADE_PATH, rule_type, name + ".js")

    if not os.path.exists(rule_location):
        raise Exception("rule file not found: {}".format(rule_location))

    with open(rule_location) as rule:
        return rule.read()
