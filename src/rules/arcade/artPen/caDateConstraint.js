// catype is anything but waiting or empty artpen_cadate needs a value
if (!haskey($feature, 'artpen_cadate') || !haskey($feature, 'artpen_catype')) {
  return true;
}

var catype = lower(domainname($feature, 'artpen_catype', $feature.artpen_catype));

if (isempty(catype)) {
  return true;
}

if (catype == 'waiting') {
  return iif(!isempty($feature.artpen_cadate), {
    'errorMessage': 'If ArtPen_CADate is populated, ArtPen_CAType should no longer be `waiting`.'
  }, true);
}

return iif(isempty($feature.artpen_cadate), {
  'errorMessage': 'ArtPen_CADate may not be empty if ArtPen_CAType has a value other than `waiting`.'
}, true);
