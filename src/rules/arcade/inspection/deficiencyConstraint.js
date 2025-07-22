if (!haskey($feature, 'inspectiondeficiency') || isempty($feature.inspectiondeficiency)) {
  return true;
}

var code = domaincode($feature, 'inspectiondeficiency', $feature.inspectiondeficiency);

if (indexof(['NO', 'OS'], code) > -1) {
  return true;
}

var correctionSet = featuresetbyname($datastore, 'uiccorrection', ['inspection_fk'], false);

var pk = $feature.guid;
var corrections = filter(correctionSet, 'inspection_fk=@pk');

return iif(isempty(corrections), {
  'errorMessage': "If InspectionDeficiency is anything other than 'No Deficiency' or 'Deficiency Not Observed' " +
    'there must be a Correction record associated with the Inspection record.'
}, true);
