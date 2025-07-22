// review date cannot be empty when ident4ca is not null
if (!haskey($feature, 'artpen_reviewdate') || !haskey($feature, 'ident4ca')) {
  return true;
}

if (isempty($feature.ident4ca) && isempty($feature.artpen_reviewdate)) {
  return true;
}

if (isempty($feature.ident4ca)) {
  return {
    'errorMessage': 'Ident4CA may not be empty if ArtPen_ReviewDate has a value.'
  }
}

return iif(isempty($feature.artpen_reviewdate), {
  'errorMessage': 'ArtPen_ReviewDate may not be empty if Ident4CA has a value.'
}, true);
