#!/usr/bin/env python
# * coding: utf8 *
"""
loader.py
A module that loads js arcade scripts into text
"""

from pathlib import Path

ARCADE_PATH = Path(__file__).resolve().parent.parent / "rules" / "arcade"


def load_rule_for(rule_type, name):
    rule_location = ARCADE_PATH / rule_type / f"{name}.js"

    if not rule_location.exists():
        raise Exception(f"rule file not found: {rule_location}")

    return rule_location.read_text()
