#!/usr/bin/env python
# * coding: utf8 *
'''
authorization.py
A module that has the UICAuthorization rules
'''

from config import config
from models.ruletypes import Constant, Calculation

create_id = '''function generateId(code, fk) {
    var field = 'CountyFIPS';
    var set = FeatureSetByName($datastore, 'UICFacility', [field], false);

    // TODO: One day there will be a relationship traversal operation
    var facilities = filter(set, 'GUID=@fk');

    if (isempty(facilities)) {
        return null;
    }

    var facility = first(facilities);

    return 'UTU' + right(facility[field], 2) + code + upper(mid($feature.guid, 29, 7));
}

var missingRequiredItems = isempty($feature.authorizationtype) || isempty($feature.facility_fk);

return iif(missingRequiredItems, null, generateId($feature.authorizationtype, $feature.facility_fk))
'''

TABLE = 'UICAuthorization'

GUID = Constant('Authorization Guid', 'GUID', 'Authorization.Guid', 'GUID()')
#: UTUCCAAXXXXXXX
#: CC = 2 digit CountyFIPS code of associated Facility
#: AA = 2 digit AuthorizationType code (https://github.com/agrc/uic-attribute-rules/issues/5)
ID = Calculation('Authorization Id', 'AuthorizationID', 'Authorization.Id', create_id)
ID.triggers = [config.triggers.insert, config.triggers.update]
