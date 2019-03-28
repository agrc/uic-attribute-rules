#!/usr/bin/env python
# * coding: utf8 *
'''
facility.py
A module that creates attribute rules for the UICFacility table
'''

from config import config
from models.ruletypes import Calculation, Constant, Constraint

extract_fips = '''var field = 'FIPS';
var set = FeatureSetByName($datastore, 'Counties', [field], true);

function getAttributeFromLargestArea(feat, set, field) {
    var items = intersects(set, feat);
    var counts = count(items);

    if (counts == 0) {
        return { 'errorMessage': 'No intersection found' };
    }

    if (counts == 1) {
        var result = first(items);

        return result[field];
    }

    var largest = -1;
    var result;

    for (var item in items) {
        var size = area(intersection(item, feat));

        if (size > largest) {
            largest = size;
            result = item[field];
        }
    }

    return result;
}

var result = getAttributeFromLargestArea($feature, set, field);

return iif(isnan(number('490' + result)), null, number('490' + result));'''

extract_city = '''var field = 'NAME';
var set = FeatureSetByName($datastore, 'Municipalities');

function getAttributeFromLargestArea(feat, set, field) {
    var items = intersects(set, feat);
    var counts = count(items);

    if (counts == 0) {
        return null;
    }

    if (counts == 1) {
        var result = first(items);

        return result[field];
    }

    var largest = -1;
    var result;

    for (var item in items) {
        var size = area(intersection(item, feat));

        if (size > largest) {
            largest = size;
            result = item[field];
        }
    }

    return result;
}

return getAttributeFromLargestArea($feature, set, field);
'''

extract_zip = '''var field = 'ZIP5';
var set = FeatureSetByName($datastore, 'ZipCodes');

function getAttributeFromLargestArea(feat, set, field) {
    var items = intersects(set, feat);
    var counts = count(items);

    if (counts == 0) {
        return { 'errorMessage': 'No intersection found' };
    }

    if (counts == 1) {
        var result = first(items);

        return result[field];
    }

    var largest = -1;
    var result;

    for (var item in items) {
        var size = area(intersection(item, feat));

        if (size > largest) {
            largest = size;
            result = item[field];
        }
    }

    return result;
}

return getAttributeFromLargestArea($feature, set, field);
'''

constrain_domain = '''var code = number($feature.countyfips)
if (isnan(code)) {
    return false
}

if (code % 2 == 0) {
    return false
}

return code >= 49001 && code <= 49057;
'''

create_id = '''return 'UTU' + right($feature.countyfips, 2) + upper(mid($feature.guid, 29, 8))'''

FACILITY_GUID = Constant('Facility Guid', 'GUID', 'Facility.Guid', 'Guid()')
FACILITY_STATE = Constant('Facility State', 'FacilityState', 'Facility.State', '"UT"')
FACILITY_FIPS = Calculation('County Fips', 'CountyFIPS', 'Facility.FIPS', extract_fips)
FACILITY_ID = Calculation('Facility Id', 'FacilityID', 'Facility.Id', create_id)
FACILITY_CITY = Calculation('Facility City', 'FacilityCity', 'Facility.City', extract_city)
FACILITY_ZIP = Calculation('Facility Zip', 'FacilityZIP', 'Facility.ZipCode', extract_zip)
FACILITY_FIPS_DOMAIN = Constraint('County Fips', 'Facility.FIPS', constrain_domain)
FACILITY_FIPS_DOMAIN.triggers = [config.triggers.insert, config.triggers.update]
