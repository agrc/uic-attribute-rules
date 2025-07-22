if (!haskey($feature, 'mitresult') || !haskey($feature, 'mittype')) {
  return true;
}

if (isempty($feature.mittype)) {
  return true;
}

return iif(isempty($feature.mitresult), {
  'errorMessage': 'MITResult may not be empty if MITType has a value.'
}, true)
