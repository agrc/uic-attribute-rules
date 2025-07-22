if (!haskey($feature, 'classifacilitytype') || !haskey($feature, 'wellclass')) {
  return true;
}

if ($feature.wellclass == 1) {
  return iif(isempty(domainname($feature, 'classifacilitytype', $feature.classifacilitytype)), {
    'errorMessage': 'ClassIFacilityType may not be empty for Class 1 wells; select the appropriate value from the UICFacilityTypeDomain (dropdown menu).'
  }, true);
}

if (isempty($feature.classifacilitytype)) {
  return true;
}

return iif(isempty(domainname($feature, 'classifacilitytype', $feature.classifacilitytype)), {
  'errorMessage': 'Acceptable values for facility type are C, N, U. Input: ' + $feature.classifacilitytype
}, true);
