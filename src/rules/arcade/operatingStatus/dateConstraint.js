if (!haskey($feature, 'OperatingStatusDate')) {
  return true;
}

if (date('1901-01-01') > $feature.operatingstatusdate || $feature.operatingstatusdate > date()) {
  return {
    'errorMessage': 'Operating status date needs to be between todays date and 1/1/1901'
  };
}

return true;
