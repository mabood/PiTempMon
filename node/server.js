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
app.get('/lineplot', function(req, res) {
    var current_date = plot.currentDate();
    res.render('pages/lineplot', {
        current_date: dateFormat(current_date, "dddd, mmmm dS, yyyy"),
        current_time: dateFormat(current_date, "h:MM TT")
    });
});

app.get('/averages', function(req, res) {
    var current_date = plot.currentDate();
    res.render('pages/averages', {
        current_date: dateFormat(current_date, "dddd, mmmm dS, yyyy"),
        current_time: dateFormat(current_date, "h:MM TT")
    });
});

app.get('/current-data', function(req, res){
   var id = req.query.id;
   var data = "";

   console.log('request: ' + req.originalUrl);

   switch (id) {
       case 'time':
           data = dateFormat(plot.currentDate(), "h:MM TT");
           break;
       case 'date':
           data = dateFormat(plot.currentDate(), "dddd, mmmm dS, yyyy");
           break;
       case 'w_tempf':
           data = plot.currentWeatherTemp() + '°';
           break;
       case 's_tempf':
           data = plot.currentSensorTemp() + '°';
           break;
       case 'w_location':
           data = plot.weatherLocation();
   }
   res.send(data);
});

app.get('/plot-data', function(req, res){
    var window = req.query.window;

    console.log('request: ' + req.originalUrl);

    var plot_data = {};
    switch(window) {
        case '12hr':
            plot_data = plot.current12hrPlot();
            break;
        case '24hr':
            plot_data = plot.current24hrPlot();
            break;
        case '2d':
            plot_data = plot.current2dPlot();
            break;
        case '5d':
            plot_data = plot.current5dPlot();
            break;
        case '10d':
            plot_data = plot.current10dPlot();
            break;
    }
    res.send(plot_data);
});

app.get('/avgs', function(req, res) {
    console.log('request: ' + req.originalUrl);

    res.send(plot.averages());
});



app.listen(8080);
console.log('8080 is the magic port');