function getAttributeFromLargestArea(feat, set, field) {
  var items = intersects(set, feat);
  var counts = count(items);

  if (counts == 0) {
    return null;
  }

  if (counts == 1) {
    var result = first(items);

    return result[field];
  }

  var largest = -1;
  var result;

  for (var item in items) {
    var size = area(intersection(item, feat));

    if (size > largest) {
      largest = size;
      result = item[field];
    }
  }

  return result;
}

function generateId(wellClass, guid, geom) {
  var field = 'FIPS';
  var set = FeatureSetByName($datastore, 'Counties', [field], true);

  var fips = getAttributeFromLargestArea(geom, set, field);

  return 'UTU' + text(fips, '00') + wellClass + upper(mid(guid, 29, 8));
}

var keys = ['wellclass', 'guid'];

for (var key in keys) {
  if (!haskey($feature, keys[key])) {
    return null;
  }
}

return iif(isempty($feature.wellclass), null, generateId($feature.wellclass, $feature.guid, geometry($feature)));
