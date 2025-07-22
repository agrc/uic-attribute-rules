if (!haskey($feature, 'ViolationType') || !haskey($feature, 'comments')) {
  return true;
}

if (isempty($feature.ViolationType) || lower(domaincode($feature, 'ViolationType', $feature.violationtype)) != 'ot') {
  return true;
}

return iif(isempty($feature.comments), {
  'errorMessage': 'When ViolationType is `Other`, enter a description of the other type of violation in the Comment field. This is required.'
}, true);
