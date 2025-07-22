if (!haskey($feature, 'remediationprojecttype')) {
  return true;
}

if (haskey($feature, 'wellsubclass') && !isempty($feature.wellsubclass) && $feature.wellsubclass == 5002 && isempty($feature.remediationprojecttype)) {
  return {
    'errorMessage': 'If WellSubClass is Subsurface Environmental Remediation well, RemediationProjectType may not be empty; select the appropriate value from the UICRemediationProjectTypeDomain (dropdown menu).'
  }
}

if (isempty($feature.remediationprojecttype)) {
  return true;
}

iif((($feature.remediationprojecttype > 0 && $feature.remediationprojecttype < 9) || $feature.remediationprojecttype == 999), true, {
  'errorMessage': 'Select the appropriate value from the UICRemediationProjectTypeDomain(dropdown menu). Input: ' + $feature.remediationprojecttype
});
