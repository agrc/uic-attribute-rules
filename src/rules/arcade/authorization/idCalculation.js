// UTUCCAAXXXXXXX
// CC = 2 digit CountyFIPS code of associated Facility
// AA = 2 digit AuthorizationType code (https://github.com/agrc/uic-attribute-rules/issues/5)

function generateId(code, fk) {
  var field = 'CountyFIPS';
  var set = FeatureSetByName($datastore, 'UICFacility', [field], false);

  // TODO: One day there will be a relationship traversal operation
  var facilities = filter(set, 'GUID=@fk');

  if (isempty(facilities)) {
    return null;
  }

  var facility = first(facilities);

  if (lower(code) == 'no') {
    code = 'UA';
  }

  return 'UTU' + right(facility[field], 2) + code + upper(mid($feature.guid, 30, 7));
}

var missingRequiredItems = isempty($feature.authorizationtype) || isempty($feature.facility_fk);

return iif(missingRequiredItems, null, generateId($feature.authorizationtype, $feature.facility_fk));
