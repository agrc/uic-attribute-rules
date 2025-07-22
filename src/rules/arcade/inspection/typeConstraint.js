if (!haskey($feature, 'inspectiontype') || !haskey($feature, 'facility_fk') || isempty($feature.inspectiontype)) {
  return true;
}

var code = lower(domaincode($feature, 'inspectiontype', $feature.inspectiontype));

if (!isempty($feature.facility_fk)) {
  // Facility Inspection Temporary or Facility Inspection No Wells
  return iif(code != 'nw' && code != 'fi', {
    'errorMessage': 'Since this is a facility inspection, InspectionType can only be Facility Inspection, No Wells or Facility Inspection Temporary.'
  }, true);
}

if (!isempty($feature.well_fk)) {
  return iif(code == 'nw' || code == 'fi', {
    'errorMessage': 'Since this is a well inspection, InspectionType can not be Facility Inspection, No Wells or Facility Inspection Temporary.'
  }, true);
}

return {
  'errorMessage': 'Facility_FK or Well_FK is required'
};
