if (!haskey($feature, 'facilityzip') || isempty($feature.facilityzip)) {
  return true;
}

return iif(isempty(domainname($feature, 'facilityzip', $feature.facilityzip)), {
  'errorMessage': 'Zip code is not in the domain. Input: ' + $feature.facilityzip
}, true);
