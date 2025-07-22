if (!haskey($feature, 'mitdate') || !haskey($feature, 'mittype')) {
  return true;
}

if (isempty($feature.mittype)) {
  return true;
}

return iif(isempty($feature.mitdate), {
  'errorMessage': 'MITDate may not be empty if MITType has a value.'
}, true);
