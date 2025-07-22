if (!haskey($feature, 'countyfips')) {
  return true;
}

var code = number($feature.countyfips)
if (isnan(code) || isempty($feature.countyfips)) {
  return {
    'errorMessage': 'The fips code is empty.'
  };
}

if (code % 2 == 0) {
  return {
    'errorMessage': 'The fips code should be odd. Input: ' + code
  };
}

if (code >= 49001 && code <= 49057) {
  return true;
}

return {
  'errorMessage': 'The code does not fall within the valid ranges: ' + code
};
