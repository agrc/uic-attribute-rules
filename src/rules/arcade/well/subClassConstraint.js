if (!haskey($feature, 'wellsubclass') || !haskey($feature, 'wellclass')) {
  return true;
}

if (isempty($feature.wellclass)) {
  return true;
}

if (isempty($feature.wellsubclass)) {
  return {
    'errorMessage': 'WellSubClass may not be empty; select the appropriate value from the UICWellSubClassDomain (dropdown menu).'
  };
}

return iif(left($feature.wellsubclass, 1) == text($feature.wellclass), true, {
  'errorMessage': 'Well sub class (' + text($feature.wellsubclass) + ') is not associated with the well class (' + text($feature.wellclass) + ')'
});
