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
						 "<br/><button onclick=\"on(\'"+ i+ "\')\">... click for more detail...</button>"
					
                    ;
				
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

var weekly_data;

function on(st_ID) {
    document.getElementById("overlay").style.display = "block";
	//document.getElementById("text").innerHTML="<h3 id=\"st_add\" style=\"margin:2px;\">" + st_ID;
	
	var path = '/weekly/'+st_ID;
	
    var xmlhttp = new XMLHttpRequest();
        xmlhttp.onreadystatechange=function() {
            if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
               
                weekly_data = JSON.parse(xmlhttp.responseText);
				drawChart();
			}
		}
        xmlhttp.open("GET", path, true);
        xmlhttp.send();
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
       infowindow.setPosition(circle.getCenter());
       infowindow.open(map);
     });
}

function hideAllMarkers(map) {
	circle.forEach(function(circle){
		circle.infowindow.close(map,circle);	   
				   });
}

////////////////////// draw stuff /////////////////////////////
function drawChart() {
	
	
				var mondaybike = 0;
				var tuesdayBike = 0;
				var wednesdayBike = 0;
				var thursdayBike = 0;
				var fridayBike = 0;
				var saturdayBike = 0;
				var sundayBike = 0;
				
				 for (i=0;i<=weekly_data.length-1;i++) {	
					 if (weekly_data[i].Weekday == 0 ) {
						 mondayBike = mondayBike + weekly_data[i].avgAvailableBikes;
					 } 	
					 else if (weekly_data[i].Weekday == 1 ) {
						 tuesdayBike = tuesdayBike + weekly_data[i].avgAvailableBikes;
					 }
					 else if (weekly_data[i].Weekday == 2 ) {
						 wednesdayBike = wednesdayBike + weekly_data[i].avgAvailableBikes;
					 }
					 else if (weekly_data[i].Weekday == 3 ) {
						 thursdayBike = thursdayBike + weekly_data[i].avgAvailableBikes;
					 }
					 else if (weekly_data[i].Weekday == 4 ) {
						 fridayBike = fridayBike + weekly_data[i].avgAvailableBikes;
					 }					 
					 else if (weekly_data[i].Weekday == 5 ) {
						 saturdayBike = saturdayBike + weekly_data[i].avgAvailableBikes;
					 }					 
					 else if (weekly_data[i].Weekday == 6 ) {
						 sundayBike = sundayBike + weekly_data[i].avgAvailableBikes;
					 }					 	 					  	
				 }
				monAvg = mondaybike;
				tuesAvg = tuesdayBike / 24;
				wedAvg= wednesdayBike / 24;
				thursAvg =  thursdayBike / 24;
				friAvg = fridayBike / 24;
				satAvg = saturdayBike / 24;
				sunAvg = sundayBike / 24;
	
	    var data = new google.visualization.arrayToDataTable([
        ['Day', 'Available Bikes'],
        ['Mon', monAvg],
        ['Tues', tuesAvg],
        ['Wed', wedAvg],
        ['Thu', thursAvg],
        ['Fri', friAvg],
        ['Sat', satAvg],
        ['Sun', sunAvg]
    ]);
	
	
	// Set display options for the chart
        var options = {
            title: 'aaaaaaaaa',
            width: 800,
            height:200,
            legend: { position: 'none' },
            chart: { title: 'Avg Bikes per Day'},
            bars: 'vertical', 
            axes: {
                y: {
                    0: { side: 'left', label: 'Bikes'} // Top x-axis.
                }
            }
        }

        // Select the HTML div element to display the chart in, and draw it
        var chart = new google.charts.Bar(document.getElementById('text'));
        chart.draw(data, options);

            }
        
	
