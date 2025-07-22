#!/usr/bin/env python
# * coding: utf8 *
"""
config.py
A module that stores common items for attribute rules
"""

from pathlib import Path
from types import SimpleNamespace

triggers = SimpleNamespace(
    **{
        "update": "UPDATE",
        "insert": "INSERT",
        "delete": "DELETE",
    }
)

rule_types = SimpleNamespace(
    **{
        "calculation": "CALCULATION",
        "constraint": "CONSTRAINT",
    }
)

editable = SimpleNamespace(
    **{
        "yes": "EDITABLE",
        "no": "NONEDITABLE",
    }
)


def get_sde_path_for(env=None):
    sde = Path(__file__).parent.parent.parent / "pro-project"

    if env is None:
        return sde / "localhost.udeq@uicadmin.sde"

    if env == "local":
        return sde / "localhost.udeq@uicadmin.sde"

    if env == "dev":
        return sde / "stage.sde"

    if env == "prod":
        return sde / "prod.sde"

    raise Exception("{} env not found".format(env))
