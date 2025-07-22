if (!haskey($feature, 'operatingstatustype') || !haskey($feature, 'operatingstatusdate')) {
  return true;
}

if (isempty($feature.operatingstatustype) && isempty($feature.operatingstatusdate)) {
  return true;
}

if (isempty($feature.operatingstatusdate)) {
  return {
    'errorMessage': 'OperatingStatusDate may not be empty when OperatingStatusType has a value.'
  }
}

return iif(isempty($feature.operatingstatustype), {
  'errorMessage': 'OperatingStatusType may not be empty when OperatingStatusDate has a value.'
}, true);
