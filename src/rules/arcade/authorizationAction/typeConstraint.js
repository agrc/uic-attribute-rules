if (!haskey($feature, 'AuthorizationActionType') || !haskey($feature, 'AuthorizationActionDate')) {
  return true;
}

if (isempty($feature.authorizationactiontype)) {
  return true;
}

return iif(isempty($feature.authorizationactiondate), {
  'errorMessage': 'AuthorizationActionDate may not be empty when AuthorizationActionType has a value.'
}, true);
