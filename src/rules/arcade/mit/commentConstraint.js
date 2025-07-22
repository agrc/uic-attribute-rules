if (!haskey($feature, 'mitremediationaction') || !haskey($feature, 'comments')) {
  return true;
}

if (isempty($feature.mitremediationaction) || lower(domainname($feature, 'mitremediationaction', $feature.mitremediationaction)) != 'other') {
  return true;
}

return iif(isempty($feature.comments), {
  'errorMessage': 'When MITRemediationAction is `Other`, enter a description of the other type of remedial action taken in the Comment field.  This is required.'
}, true);
