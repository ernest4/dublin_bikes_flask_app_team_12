var station="";
var infoBox = "";
function initialize() {

    var mapOptions = {
        center:new google.maps.LatLng(53.3498,-6.2603),
        zoom:13,
        mapTypeId:google.maps.MapTypeId.ROADMAP,
        scrollwheel:false
    };


    var map=new google.maps.Map(document.getElementById("dublin_map"),mapOptions);


    var url="/jcdapi"

    // Station coordinates are retrieved from JSON  data
    var xmlhttp = new XMLHttpRequest();
        xmlhttp.onreadystatechange=function() {
            if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
                data = JSON.parse(xmlhttp.responseText);
				console.log(data);

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

                    infoBox =
                        "<h3 id=\"st_add\" style=\"margin:2px;\">" + 
                        data[i].address + 
                        "</h2><span style=\"text-align:center;font-size:10px;color:black;\">Bikes: " + data[i].available_bikes + "</br>Docking Stations: " 
                        + data[i].available_bike_stands +
						// "<br/><button onclick=\"on("+data[i].available_bikes+")\">... click for more detail...</button>"    
					// passing an int works but not a string ??
						 "<br/><button onclick=\"on(\'"+ data[i].address+ "\')\">... click for more detail...</button>"
					
                    ;
					console.log(data[i].address)
                   makeClickable(map, circle, infoBox);
                }
            }
        }
        xmlhttp.open("GET", url, true);
        xmlhttp.send();
}


	///////////////////////////////////
	////////////// overlay ////////////
	///////////////////////////////////


function on(number) {
    document.getElementById("overlay").style.display = "block";
	document.getElementById("text").innerHTML="<h3 id=\"st_add\" style=\"margin:2px;\">" + number;
	
}

function off() {
    document.getElementById("overlay").style.display = "none";
	// run query on database 
	// select all from DB where num = num;
	// getElementByID
}

	///////////////////////////////////
	///////////////////////////////////
	///////////////////////////////////


function makeClickable(map, circle, info) {

     var infowindow = new google.maps.InfoWindow({
         content: info

     });
   
     google.maps.event.addListener(circle, 'click', function(ev) {
//	 var currentInfoWindow = null;
//	   if (currentInfoWindow != null) {
//		   currentInfoWindow.close();
//	   }
       infowindow.setPosition(circle.getCenter());
       infowindow.open(map);
	  // currentInfoWindow = infowindow;
     });
}

function hideAllMarkers(map) {
	circle.forEach(function(circle){
		circle.infowindow.close(map,circle);	   
				   });
}

