curl -X POST -H 'content-type: application/json' -d '{
  "origin": {
    "address":"[ORIG]"
  },
  "destination": {
    "address":"[DEST]"
  },
  "travelMode": "TRANSIT",
  "computeAlternativeRoutes": false,
  "transitPreferences": {
     routingPreference: "LESS_WALKING"
  },
}' \
-H 'Content-Type: application/json' \
-H 'X-Goog-Api-Key: [MAP_KEY] \
-H 'X-Goog-FieldMask: routes.localizedValues' \
'https://routes.googleapis.com/directions/v2:computeRoutes'