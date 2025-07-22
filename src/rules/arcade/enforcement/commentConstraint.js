if (!haskey($feature, 'EnforcementType') || !haskey($feature, 'comments')) {
  return true;
}

if (isempty($feature.EnforcementType) || lower(domaincode($feature, 'EnforcementType', $feature.enforcementtype)) != 'otr') {
  return true;
}

return iif(isempty($feature.comments), {
  'errorMessage': 'When EnforcementType is `Other`, enter a description of the other type of enforcement action taken in the Comment field. This is required.'
}, true);
