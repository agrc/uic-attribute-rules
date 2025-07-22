if (!haskey($feature, 'facility_fk') || !haskey($feature, 'well_fk')) {
  return true;
}

return iif(isempty($feature.facility_fk) && isempty($feature.well_fk) || (!isempty($feature.facility_fk) && !isempty($feature.well_fk)), {
  'errorMessage': 'A violation record must have either, but not both, a Facility_FK or a Well_FK.'
}, true);
