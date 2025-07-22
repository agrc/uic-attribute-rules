if (!haskey($feature, 'highpriority') || !haskey($feature, 'wellclass')) {
  return true;
}

if ($feature.wellclass == 5) {
  return iif(isempty(domainname($feature, 'highpriority', $feature.highpriority)), {
    'errorMessage': 'HighPriority may not be empty for Class V wells; select the appropriate value from the UICYesNoUnknownDomain (dropdown menu).'
  }, true);
}

if (isempty($feature.highpriority)) {
  return true;
}

return iif(isempty(domainname($feature, 'highpriority', $feature.highpriority)), {
  'errorMessage': 'Acceptable values for high priority are Y, N, U. Input: ' + $feature.highpriority
}, true);
