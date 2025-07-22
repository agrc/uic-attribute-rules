if (!haskey($feature, 'mitremediationaction') || !haskey($feature, 'mitresult')) {
  return true;
}

if (isempty($feature.mitresult) || lower(domainname($feature, 'mitresult', $feature.mitresult)) == 'pass') {
  return true;
}

return iif(isempty($feature.mitremediationaction), {
  'errorMessage': 'MITRemediationAction may not be empty if MITResult has a value other than `Pass`. ' +
    'If waiting for remedial action to be performed, select `waiting` from the UICMITRemediationActionDomain (dropdown menu).'
}, true);
