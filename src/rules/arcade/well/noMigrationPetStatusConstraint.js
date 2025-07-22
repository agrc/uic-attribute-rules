// if well class is empty, no worries
if (!haskey($feature, 'wellsubclass') || isempty($feature.wellsubclass)) {
  return true;
}

// if well class is not 1001, no worries
if ($feature.wellsubclass != 1001) {
  return true;
}

return iif(isempty($feature.nomigrationpetstatus) || lower(domaincode($feature, 'nomigrationpetstatus', $feature.nomigrationpetstatus)) == 'na', {
  'errorMessage': 'NoMigrationPetStatus for Class I Hazardous wells may not be empty nor may it be `Not Applicable`. Select the appropriate value from the UICNoMigrationPetStatusDomain (dropdown menu).'
}, true);
