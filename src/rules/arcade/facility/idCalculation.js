var keys = ['countyfips', 'guid'];

for (var key in keys) {
  if (!haskey($feature, keys[key])) {
    return null;
  }
}

return 'UTU' + right($feature.countyfips, 2) + 'F' + upper(mid($feature.guid, 29, 8))
