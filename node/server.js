// server.js
// load the things we need
var express = require('express');
var path = require('path');
var app = express();
//var Promise = require('promise');
var plot = require('./plotReader');

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
    res.render('pages/index', {
        current_sensor: current_sensor,
        current_weather: current_weather,
        current_date: dateFormat(current_date, "dddd, mmmm dS, yyyy, h:MM:ss TT")
    });
});

// about page
app.get('/about', function(req, res) {
    res.render('pages/about');
});

// about page
app.get('/lineplot', function(req, res) {
    var current_temp = "68";//(String(68.5) + '°');
    res.render('pages/lineplot', {
       current_temp: current_temp
    });
});

app.get('/12hr-data', function(req, res){
    var plot_12hr = plot.current12hrPlot();

    // input value from search
    var val = req.query.search;
    console.log(plot_12hr);

    res.send(plot_12hr);

});

app.get('/24hr-data', function(req, res){
    var plot_24hr = plot.current24hrPlot();

    // input value from search
    var val = req.query.search;
    console.log(plot_24hr);

    res.send(plot_24hr);

});

app.listen(8080);
console.log('8080 is the magic port');