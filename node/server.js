// server.js
// load the things we need
var express = require('express');
var path = require('path');
var app = express();
//var Promise = require('promise');
var plot = require('./plotReader');
var dateFormat = require('dateformat');

app.set('views', path.join(__dirname, '/public/views'));

// set the view engine to ejs
app.set('view engine', 'ejs');



// index page
app.get('/', function(req, res) {
    var current_sensor = plot.currentSensorTemp() + '°';
    var current_weather = plot.currentWeatherTemp() + '°';
    var plot_12hr = plot.current12hrPlot();
    var plot_24hr = plot.current24hrPlot();
    var current_date = plot.currentDate();
    var weather_location = plot.weatherLocation();
    res.render('pages/index', {
        current_sensor: current_sensor,
        current_weather: current_weather,
        current_date: dateFormat(current_date, "dddd, mmmm dS, yyyy"),
        current_time: dateFormat(current_date, "h:MM TT"),
        weather_local: weather_location
    });
});

// about page
app.get('/about', function(req, res) {
    var current_date = plot.currentDate();
    res.render('pages/about', {
        current_date: dateFormat(current_date, "dddd, mmmm dS, yyyy"),
        current_time: dateFormat(current_date, "h:MM TT")
    });
});

// about page
app.get('/lineplot', function(req, res) {
    var current_date = plot.currentDate();
    res.render('pages/lineplot', {
        current_date: dateFormat(current_date, "dddd, mmmm dS, yyyy"),
        current_time: dateFormat(current_date, "h:MM TT")
    });
});

app.get('/plot-data', function(req, res){

    var window = req.window;
    switch (window) {
        case "12hr":
            res.send(plot.current12hrPlot());
            break;
        case "24hr":
            res.send(plot.current24hrPlot());
            break;
        case "2d":
            res.send(plot.current2dPlot());
            break;
        case "5d":
            res.send(plot.current5dPlot());
            break;
        case "10d":
            res.send(plot.current10dPlot());
            break;

    }

});


app.listen(8080);
console.log('8080 is the magic port');