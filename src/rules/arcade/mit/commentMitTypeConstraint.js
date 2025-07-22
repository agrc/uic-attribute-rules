if (!haskey($feature, 'mittype') || !haskey($feature, 'comments')) {
  return true;
}

var mitType = lower(domainname($feature, 'mittype', $feature.mittype));

if (isempty($feature.mittype)) {
  return true;
}

var otherTypes = ['1 - other significant leak test', '2 - other fluid migration test'];

if (indexof(otherTypes, mitType) == -1) {
  return true;
}

return iif(isempty($feature.comments), {
  'errorMessage': 'If MITType is `1 - other significant leak test` or `2 - other fluid migration test`, describe the alternative MIT method in the Comments field.'
}, true);
