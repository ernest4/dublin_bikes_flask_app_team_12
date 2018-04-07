// B
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
	google.charts.load('current', {'packages':['corechart']});
	
	//google.charts.setOnLoadCallback();
	var xmlhttp = new XMLHttpRequest();
        xmlhttp.onreadystatechange=function() {
            if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
               
                weekly_data = JSON.parse(xmlhttp.responseText);
				google.charts.setOnLoadCallback(drawChart);
	
				
			}
		}
        xmlhttp.open("GET", path, true);
        xmlhttp.send();
	
}


function off() {
    document.getElementById("overlay").style.display = "none";

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
		var aBikes = [
		[0],[1],[2],[3],[4],[5],[6],[7],[8],[9],[10],[11],[12],[13],[14],[15],[16],[17],[18],[19],[20],[21],[22],[23]
		];
		for (i=0; i< weekly_data.length; i++){
			for (j=0;j<24; j++){
			if(weekly_data[i].Hour == j) 
				aBikes[j].push(weekly_data[i].avgAvailableBikes)
			}
		}	
	    var data = google.visualization.arrayToDataTable([
        ['Hour', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
        aBikes[0],aBikes[1],aBikes[2],aBikes[3],aBikes[4],aBikes[5],aBikes[6],aBikes[7],
		aBikes[8],aBikes[9],aBikes[10],aBikes[11],aBikes[12],aBikes[13],aBikes[14],aBikes[15],
		aBikes[16],aBikes[17],aBikes[18],aBikes[19],aBikes[20],aBikes[21],aBikes[22],aBikes[23]
    ]);
	
	
	// Set display options for the chart
      var options = {
          title: 'Weekly Occupancy Data (Number of Available Bikes)',
          hAxis: {title: 'Hour',  titleTextStyle: {color: '#333'}},
          vAxis: {minValue: 0},
          isStacked: "true",
		  width :600,
          height:200
        };
	
	    var chart = new google.visualization.AreaChart(document.getElementById('text'));
        chart.draw(data, options);

            }
        
