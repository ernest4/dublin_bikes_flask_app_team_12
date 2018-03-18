// Function to create a map (called when page loads)
function initialize() {
    // Define properties of the map
    var mapOptions = {
        center:new google.maps.LatLng(53.3498,-6.2603),
        zoom:13,
        mapTypeId:google.maps.MapTypeId.ROADMAP,
        scrollwheel:false
    };

    // This will display on the left hand of the page
    var map=new google.maps.Map(document.getElementById("dublin_map"),mapOptions);

    // Information for API call
	// Colins key
    var NAME="Dublin";
    var APIKEY="b3cd5493b4afcaa34ec3f98453204675c656cb35";
    var url="https://api.jcdecaux.com/vls/v1/stations?contract=" + NAME + "&apiKey=" + APIKEY;

    // Station coordinates are retrieved from JSON  data 
    var xmlhttp = new XMLHttpRequest();
        xmlhttp.onreadystatechange=function() {
            if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
                data = JSON.parse(xmlhttp.responseText);
	
                for (i=0;i<=data.length;i++) {

                    var colour;
       
                    if (data[i].available_bikes/data[i].bike_stands == 0) {
                        colour = 'red';
                    }else if (0.2 <= data[i].available_bikes/data[i].bike_stands > 0.9) {
                        colour = 'orange';
                    } else {
                        colour = 'green';
                    };
                    // markers on map 
                    circle = new google.maps.Circle({
                        strokeColor: colour,
                        strokeOpacity: '0.8',
                        strokeWeight: 2,
                        fillColor: colour,
                        fillOpacity: 0.25,
                        map: map,
                        radius: 75,
                        clickable:true,
                        center: {lat: data[i].position.lat, lng: data[i].position.lng},
                    });
                    makeClickable(map, circle);
                }
            }
        }
        xmlhttp.open("GET", url, true);
        xmlhttp.send();
}

 function makeClickable(map, circle, info) {
     var infowindow = new google.maps.InfoWindow({
         content: info
     });
 }

