var station="";
var infoBox = "";
var activeinfowindow;
var markers = [];
var marker;
var weekly_data;
var analytic_data;

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
                for (var i=0;i<=data.length;i++) {
                    var colour;
					try {
						var bikes = data[i].available_bikes;
						var stands = data[i].bike_stands;
						var position = {lat: data[i].position.lat, lng: data[i].position.lng};
						var address = data[i].address;
					} catch(e){
						if(e){
							console.log("Do something!")
						}
					}
                    if (bikes/stands < 0.1) {
                        colour = 'red';	
                    }else if (0.1 <= bikes/stands  && bikes/stands <= 0.8) {
                        colour = 'orange';
                    } else {
                        colour = 'green';
                    };
                   marker = new google.maps.Marker({
                        position: position,
                        map: map,
                        icon: 'http://maps.google.com/mapfiles/ms/icons/' + colour +'-dot.png',
					    animation: google.maps.Animation.DROP
                    });
					
                    infoBox =
					     "<h3 id=\"st_add\" style=\"margin:2px;color:black;font-size:16px;text-align: center;\">" +
                         address + "</h3></br><div style=\"color:black;font-size:25px;text-align: center;\">" +bikes +"&ensp;&ensp;|&ensp;&ensp;"+stands +
 						"</br> bikes&emsp;stands</div> " +
						 "<br/><button class=btn   style=\"float: left;\"   onclick=\"on2(\'"+ i+ "\')\">&#x2614</button >&ensp;&ensp;<button class=btn style=\"float: right;\"  onclick=\"on(\'"+ i+ "\')\"> &#x1F4C8</button>";
                   makeClickable(map, marker, infoBox);
                }
            }
        }
        xmlhttp.open("GET", url, true);
        xmlhttp.send();
}
function on(st_ID) {
    document.getElementById("overlay").style.display = "block";
	var path = '/weekly/'+st_ID;
	google.charts.load('current', {'packages':['corechart']});
	var xmlhttp = new XMLHttpRequest();
        xmlhttp.onreadystatechange=function() 
		{
            if (xmlhttp.readyState == 4 && xmlhttp.status == 200) 
			{
                weekly_data = JSON.parse(xmlhttp.responseText);
				google.charts.setOnLoadCallback(drawChart);
			}
		}
        xmlhttp.open("GET", path, true);
        xmlhttp.send();
}
//////////////////////////////////////////////////////////////////////////////
function on2(st_ID) {
    document.getElementById("overlay").style.display = "block";
	var path = '/analytic/'+st_ID;
	google.charts.load('current', {'packages':['corechart']});
	var xmlhttp = new XMLHttpRequest();
        xmlhttp.onreadystatechange=function() 
		{
            if (xmlhttp.readyState == 4 && xmlhttp.status == 200) 
			{
                analytic_data = JSON.parse(xmlhttp.responseText);
				google.charts.setOnLoadCallback(drawChart2);
			}
		}
        xmlhttp.open("GET", path, true);
        xmlhttp.send();
}

function off() {
    document.getElementById("overlay").style.display = "none";
}
function makeClickable(map, marker, info) { 
   	var infowindow = new google.maps.InfoWindow({
         content: info        
     });	
     google.maps.event.addListener(marker, 'click', function() {   
		marker.setAnimation(google.maps.Animation.BOUNCE);
		map.panTo(marker.getPosition());
     if(activeinfowindow) {activeinfowindow.close();}
        infowindow.open(map,marker);
        activeinfowindow = infowindow;     
     });
	
	marker.addListener('click', function () {
    marker.setAnimation(null);
});
}
function toggleBounce() {
        if (marker.getAnimation() !== null) {
          marker.setAnimation(null);
        } else {
          marker.setAnimation(google.maps.Animation.BOUNCE);
        }
}
function drawChart()
{
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
      var options = 
		  {
          title: 'Average Available Bikes',
          hAxis: {title: 'Hour',  titleTextStyle: {color: '#333'},
				  ticks:[1,3,5,7,9,11,13,15,17,19,21,23]},
          vAxis: {title: 'Bikes',minValue: 0, maxValue:100,
				 	},
          isStacked: "true",
		 // backgroundColor: { fill:'transparent' },
		  width :1000,
          height:400
        };
	    var chart = new google.visualization.AreaChart(document.getElementById('text'));
        chart.draw(data, options);
}
/////////////////////////////////////////////////////////////////////////////////////
function drawChart2()
{
		var bBikes = new Array(24);
		var tickz = new Array(24);
		for (i=0; i < analytic_data.length; i++){
				bBikes[i] = new Array(2);
				bBikes[i][0] =''+ analytic_data[i].Hour;
				bBikes[i][1] = analytic_data[i].avgAvailableBikes;	
		}
	console.log(tickz);
	    var data2 = google.visualization.arrayToDataTable([
        ['Hour', 'available'],
        bBikes[0],bBikes[1],bBikes[2],bBikes[3],bBikes[4],bBikes[5],bBikes[6],bBikes[7],
		bBikes[8],bBikes[9],bBikes[10],bBikes[11],bBikes[12],bBikes[13],bBikes[14],bBikes[15],
		bBikes[16],bBikes[17],bBikes[18],bBikes[19],bBikes[20],bBikes[21],bBikes[22],bBikes[23]
    ], false);
      var options2 = 
		  {
          title: 'Inclement Weather Hourly Averages ',
          hAxis: {title: 'hours from now',  titleTextStyle: {color: '#333'}},
          vAxis: {title: 'Bikes'
				 	},
          isStacked: "true",
		 // backgroundColor: { fill:'transparent' },
		  width :1000,
          height:400
        };
	    var chart2 = new google.visualization.AreaChart(document.getElementById('text'));
        chart2.draw(data2, options2);
}