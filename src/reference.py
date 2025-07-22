#!/usr/bin/env python
# * coding: utf8 *
"""
reference

Usage:
    reference refresh [--env=<env>]
    reference --version
    reference (-h | --help)

Options:
    --env=<env>     local, dev, prod
    -h --help       Shows this screen
    -v --version    Shows the version
"""

from pathlib import Path

import arcpy
from docopt import docopt

from config.config import get_sde_path_for


def import_sgid_data(sde):
    """
    Imports SGID data for municipalities, zip codes, and county boundaries
    into the specified environment (staging or production).
    """
    # Define SGID source tables
    sgid_tables = {
        "Municipalities": "https://services1.arcgis.com/99lidPhWCzftIe9K/ArcGIS/rest/services/UtahMunicipalBoundaries/FeatureServer/0",
        "ZipCodes": "https://services1.arcgis.com/99lidPhWCzftIe9K/ArcGIS/rest/services/UtahZipCodeAreas/FeatureServer/0",
        "Counties": "https://services1.arcgis.com/99lidPhWCzftIe9K/ArcGIS/rest/services/UtahCountyBoundaries/FeatureServer/0",
    }

    for name, sgid_path in sgid_tables.items():
        target_fc = f"{sde}\\{name}"
        print(f"Refreshing {sgid_path} to {target_fc}...")

        # Truncate the target feature class before appending new data
        arcpy.management.TruncateTable(target_fc)
        arcpy.management.Append(sgid_path, target_fc, "NO_TEST")


def main():
    """Main entry point for program. Parse arguments and pass to engine module"""
    args = docopt(__doc__, version="2025.07.21")

    sde = get_sde_path_for(args["--env"])
    print("acting on {}".format(sde))

    test_table = str(sde / "Municipalities")
    if not arcpy.TestSchemaLock(test_table):
        print("Unable to reach the database or acquire the necessary schema lock to update data", test_table)
        exit(0)

    import_sgid_data(sde)


if __name__ == "__main__":
    main()
