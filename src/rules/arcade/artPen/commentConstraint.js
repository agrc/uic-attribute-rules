if (!haskey($feature, 'artpen_catype') || !haskey($feature, 'comments')) {
  return true;
}

var catype = lower(domainname($feature, 'artpen_catype', $feature.artpen_catype));

if (isempty(catype)) {
  return true;
}

return iif(catype == 'other ca method' && isempty($feature.comments), {
  'errorMessage': 'If ArtPen_CAType is `other CA method`, then describe the alternate CA method in the comments field.'
}, true);
