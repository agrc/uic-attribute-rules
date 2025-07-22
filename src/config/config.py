#!/usr/bin/env python
# * coding: utf8 *
"""
config.py
A module that stores common items for attribute rules
"""

import os
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
    sde = os.path.join(os.path.dirname(__file__), "..", "..", "pro-project")

    if env is None:
        return os.path.join(sde, "localhost.udeq@uicadmin.sde")

    if env == "local":
        return os.path.join(sde, "localhost.udeq@uicadmin.sde")

    if env == "dev":
        return os.path.join(sde, "stage.sde")

    if env == "prod":
        return os.path.join(sde, "prod.sde")

    raise Exception("{} env not found".format(env))
