// Creating map object
var myMap = L.map("map", {
  center: [39.8283, -98.5795],
  zoom: 11
});

// Adding tile layer to the map
L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
  attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
  maxZoom: 18,
  id: "mapbox.streets",
  accessToken: API_KEY
}).addTo(myMap);

d3.json("/scrape").then((data) => {
 // Create a new marker cluster group
 var markers = L.markerClusterGroup();

 // Loop through data
 for (var i = 0; i < data.length; i++) {

   // Set the data location property to a variable
   var latitude = data.Store_Latitude[i];
   var longitude = data.Store_Longitude[i];

   // Check for location property
   if (latitude && longitude) {

     // Add a new marker to the cluster group and bind a pop-up
     markers.addLayer(L.marker([latitude, longitude])
       .bindPopup(data.Store_Name[i]));
   }

 }

 // Add our marker cluster layer to the map
 myMap.addLayer(markers);
});

