// current weather for Dublin from openweather api
$( document ).ready(function() {
        getWeather();
    });
function getWeather(){
    var weatherdata;
    $.getJSON('http://api.openweathermap.org/data/2.5/weather?q=dublin,ie&units=metric&appid=b7ec756c9f034d4b7ed08256263bf6a3',function(data){
    var currentWeather = data.weather[0].description;
    var current_temp=data.main.temp;
    var wind_speed=data.wind.speed;
    var icon = data.weather[0].icon;
    var iconUrl = ("<img src='http://openweathermap.org/img/w/" + icon + ".png'>");
    $("#icon").html(iconUrl);
    $("#currentWeather").html(currentWeather);
    $("#currentTemp").html(current_temp + "&#8451");
    $("#windspeed").html(wind_speed + "m&#178;");   
});
}
