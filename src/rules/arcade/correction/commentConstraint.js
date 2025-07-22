if (!haskey($feature, 'correctiveaction') || !haskey($feature, 'comments')) {
  return true;
}

if (isempty($feature.correctiveaction) || lower(domaincode($feature, 'correctiveaction', $feature.correctiveaction)) != 'ot') {
  return true;
}

return iif(isempty($feature.comments), {
  'errorMessage': 'When CorrectiveAction is `Other`, enter a description of the other type of corrective action to be taken in the Comment field. This is required.'
}, true);
