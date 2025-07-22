if (!haskey($feature, 'inspectiondate') || !haskey($feature, 'well_fk') || isempty($feature.inspectiondate)) {
  return true;
}

if (isempty($feature.well_fk)) {
  return true;
}

var well = $feature.well_fk;
var statusSet = featuresetbyname($datastore, 'UICWellOperatingStatus', ['OperatingStatusDate'], false);

var statuses = filter(statusSet, 'well_fk=@well');

if (isempty(statuses)) {
  return true;
}

var earliestDate = date();

for (var status in statuses) {
  if (status.operatingstatusdate < earliestDate) {
    earliestDate = status.operatingstatusdate;
  }
}

return iif($feature.inspectiondate < earliestDate, {
  'errorMessage': 'If the Inspection record is associated with a Well, the InspectionDate must be equal ' +
    'to or later than the earliest OperatingStatusDate associated with the Well.'
}, true);
