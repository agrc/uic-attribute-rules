if (!haskey($feature, 'AuthorizationActionDate') || isempty($feature.AuthorizationActionDate)) {
  return true;
}

var field = 'StartDate';
var set = FeatureSetByName($datastore, 'UICAuthorization', [field], false);

var fk = $feature.authorization_fk;

// TODO: One day there will be a relationship traversal operation
var authorizations = filter(set, 'GUID=@fk');

if (isempty(authorizations)) {
  return true;
}

var authorization = first(authorizations);

return iif($feature.AuthorizationActionDate < authorization.startdate, {
  'errorMessage': 'AuthorizationActionDate must be no earlier than the StartDate of the associated Authorization record'
}, true);
