// ident4ca is yes artpen_catype cannot be empty
if (!haskey($feature, 'artpen_catype') || !haskey($feature, 'ident4ca')) {
  return true;
}

var no = 2;

if (isempty($feature.ident4ca) || $feature.ident4ca == no) {
  return true;
}

return iif(isempty($feature.artpen_catype), {
  'errorMessage': 'ArtPen_CAType may not be empty if Ident4CA has a value other than `no`. If waiting for corrective action to be performed, select `waiting` from the UICArtPenCAType domain (dropdown menu).'
}, true);
