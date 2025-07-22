if (!haskey($feature, 'mitremactdate') || !haskey($feature, 'mitdate')) {
  return true;
}

var earliestDate = date();

return iif($feature.mitremactdate > earliestDate || $feature.mitremactdate < $feature.mitdate, {
  'errorMessage': 'The MIT Rem Act Date must be between the MIT Date and today\'s date.'
}, true);
