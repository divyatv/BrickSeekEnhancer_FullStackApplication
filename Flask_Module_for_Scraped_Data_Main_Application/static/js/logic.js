//Creating map object
var myMap = L.map("map", {
    center: [39.8283, -98.5795],
    zoom: 5
  });
  
  // Adding tile layer to the map
  L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
    attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
    maxZoom: 15,
    id: "mapbox.streets",
    accessToken: API_KEY
  }).addTo(myMap);
    
  console.log(graphData)
   // Create a new marker cluster group
   var markers = L.markerClusterGroup();
  
   // Loop through data
   for (var i = 0; i < graphData.length; i++) {
  
     // Set the data location property to a variable
     var latitude = graphData[i].Store_Latitude;
     var longitude = graphData[i].Store_Longitude;
  
     // Check for location property
     if (latitude && longitude) {
  
       // Add a new marker to the cluster group and bind a pop-up
       markers.addLayer(L.marker([latitude, longitude])
         .bindPopup("Store Name: " + graphData[i].Store_Name + "<br> Availability: " + graphData[i].Item_Availability + "<br> Discount: " + graphData[i].Item_Discount + " | Price: " + graphData[i].Item_Price + "<br> <a href="+ "'" + graphData[i].Google_Maps + "'" + "target='_blank'>" + "Directions"+"</a>")).on('mouseover',function(ev) {
          ev.target.openPopup(graphData[i].Item_Quantity);
      //  markers.on('mouseover',function(ev) {
      //     ev.target.openPopup(graphData[i].priceoff);
       });
     }
  
   }
  
   // Add our marker cluster layer to the map
   myMap.addLayer(markers);