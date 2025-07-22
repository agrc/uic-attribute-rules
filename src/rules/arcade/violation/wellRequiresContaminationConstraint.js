if (!haskey($feature, 'well_fk') || !haskey($feature, 'usdwcontamination')) {
  return true;
}

return iif(!isempty($feature.well_fk) && isempty(domainname($feature, 'usdwcontamination', $feature.usdwcontamination)), {
  'errorMessage': 'Wells need a USDW Contamination value'
}, true);
