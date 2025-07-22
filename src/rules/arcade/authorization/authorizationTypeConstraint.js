return iif(lower($feature.AuthorizationType) == 'no', {
  'errorMessage': 'AuthorizationType may not be `Unauthorized`; select the appropriate value from the UICAuthorizeTypeDomain (dropdown menu).'
}, true);
