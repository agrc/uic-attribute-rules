if (!haskey($feature, 'mitremactdate') || !haskey($feature, 'mitremediationaction')) {
  return true;
}

if (lower(domainname($feature, 'mitremediationaction', $feature.mitremediationaction)) == 'waiting') {
  return iif(!isempty($feature.MITRemActDate), {
    'errorMessage': 'If MITRemActDate is populated, MITRemediationAction should no longer be `waiting`'
  }, true)
}

return iif(isempty($feature.mitremactdate), {
  'errorMessage': 'MITRemActDate may not be empty if MITRemediationAction has a value other than `waiting`.'
}, true);
