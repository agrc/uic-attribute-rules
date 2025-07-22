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

var field = 'Guid';
var set = FeatureSetByName($datastore, 'UICFacility', [field], true);

if (!haskey($feature, field)) {
  return null;
}

return getAttributeFromLargestArea($feature, set, field);
