if (!haskey($feature, 'enforcementtype') || !haskey($feature, 'enforcementdate')) {
  return true;
}

if (isempty($feature.enforcementtype)) {
  return true;
}

return iif(isempty($feature.enforcementdate), {
  'errorMessage': 'EnforcementDate may not be null when EnforcementType has a value.'
}, true);
