var station="";
var infoBox = "";
var markers = [];
function initialize() {
    var mapOptions = {
        center:new google.maps.LatLng(53.3498,-6.2603),
        zoom:14,
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

				////////////// console.log  //////////////
				//////////////////////////////////////////				


	
				//////////////////////////////////////////
				
				
				
                for (i=0;i<=data.length;i++) {

                    var colour;
                    if (data[i].available_bikes/data[i].bike_stands < 0.2) {
                        colour = 'red';
                    }else if (0.2 <= data[i].available_bikes/data[i].bike_stands && data[i].available_bikes/data[i].bike_stands <= 0.8) {
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
                        fillOpacity: .001,
                        map: map,
                        radius: 100,
                        clickable:true,
                        center: {lat: data[i].position.lat, lng: data[i].position.lng},
                    });
                    infoBox =

//                        "<h3 id=\"st_add\" style=\"margin:2px;\">" + 
//                        data[i].address + 
//                        "</h2><span style=\"text-align:center;font-size:10px;color:black;\">Bikes: " + data[i].available_bikes + "</br>Docking Stations: " 
//                        + data[i].available_bike_stands +
//						 "<br/><button onclick=\"on("+i+")\">... click for more detail...</button>"    
//					// passing an int works but not a string ??
//						// "<br/><button onclick=\"on(\'"+ data[i].address+ "\')\">... click for more detail...</button>"
//					

                        "<h3 id=\"st_add\" style=\"margin:2px;color:black;font-size:16px;text-align: center;\">" +
                        data[i].address + "</h3></br><div style=\"color:black;font-size:25px;text-align: center;\">" +data[i].available_bikes +"&ensp;&ensp;|&ensp;&ensp;"+data[i].available_bike_stands +
						"</br> bikes&emsp;stands</div> " +
						 "<br/><button class=btn   style=\"float: left;\"   onclick=\"on(\'"+ i+ "\')\">&#x2614</button >&ensp;&ensp;<button class=btn style=\"float: right;\"  onclick=\"on(\'"+ i+ "\')\"> &#x1F4C8</button>"

                    ;
                   makeClickable(map, circle, infoBox);
                }
            }
        }
        xmlhttp.open("GET", url, true);
        xmlhttp.send();
}



	//////////////////////////////////////////
	////////////// from analytics: ///////////
	//////////////////////////////////////////

// global variable (numbers for graphs)

	///////////////////////////////////
	////////////// overlay ////////////
	///////////////////////////////////


var weekly_data;

function on(st_ID) {
    document.getElementById("overlay").style.display = "block";
	document.getElementById("text").innerHTML="<h3 id=\"st_add\" style=\"margin:2px;\">" + st_ID;
	
	var path = '/weekly/' + st_ID;  // --> "/weekly/69"
	    var xmlhttp = new XMLHttpRequest();
        xmlhttp.onreadystatechange=function() {
            if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
                
                weekly_data = JSON.parse(xmlhttp.responseText);
          		console.log(weekly_data);
				// this function will generate the visuals
                drawGraph();
            }
        }
        xmlhttp.open("GET", path, true);
        xmlhttp.send();

	
	
	// run query on database 
	// select all from DB where num = num;
	// getElementByID
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
	///////// Clickable Map ///////////
	///////////////////////////////////

var infowindow;
function makeClickable(map, circle, info) {

     infowindow = new google.maps.InfoWindow({
         content: info
     });
     google.maps.event.addListener(circle, 'click', function(ev) {

		
		hideAllInfoWindows(map);
       infowindow.setPosition(circle.getCenter());
	   map.panTo(circle.getCenter());
       infowindow.open(map);
     });
	markers.push(circle);
}

function hideAllInfoWindows(map) {
	markers.forEach(function(circle){
		infowindow.close(map,circle);
				   });
}

////////////////////// draw stuff /////////////////////////////
function drawChart() {
		var aBikes = [
		[0],[1],[2],[3],[4],[5],[6],[7],[8],[9],[10],[11],[12],[13],[14],[15],[16],[17],[18],[19],[20],[21],[22],[23]
		];
	// This loop populates the 2D list of times and average available bikes
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
          title: 'Average Available Bikes',
          hAxis: {title: 'Hour',  titleTextStyle: {color: '#333'},
				  // 'tick' values are the numerical values that are displayed on the x and y axis
				  ticks:[1,3,5,7,9,11,13,15,17,19,21,23]},
          vAxis: {title: 'Bikes',minValue: 0, maxValue:140,
				 	ticks: [0,20,40,60,80,100,120,140,160]},
          isStacked: "true",
		  width :1000,
          height:400
        };

	    var chart = new google.visualization.AreaChart(document.getElementById('text'));
        chart.draw(data, options);

            }
