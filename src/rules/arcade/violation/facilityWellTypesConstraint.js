if (!haskey($feature, 'ViolationType') || !haskey($feature, 'Well_FK') || !haskey($feature, 'Facility_FK')) {
  return true;
}

var facilityViolations = ['OM', 'MR', 'FO', 'FA', 'FI', 'FR', 'OT'];
var wellViolations = ['UI', 'OM', 'PA', 'MR', 'IP', 'FO', 'FA', 'FR', 'MI', 'MO', 'OT'];

if (!isempty($feature.well_fk)) {
  return iif(indexof(wellViolations, $feature.violationtype) == -1, {
    'errorMessage': 'Acceptable well violation types: ' + wellViolations
  }, true);
}

if (!isempty($feature.facility_fk)) {
  return iif(indexof(facilityViolations, $feature.violationtype) == -1, {
    'errorMessage': 'Acceptable facility violation types: ' + facilityViolations
  }, true);
}
