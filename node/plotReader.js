/**
 * Created by MikeGA on 2/13/17.
 */
var fs = require('fs');
var moment = require('moment-timezone');


function readJSON(filename){
    var contents = fs.readFileSync(filename);
    // Define to JSON type
    return JSON.parse(contents);
}

function convert_time_utc(timestamp) {
    return moment.tz(timestamp, moment.tz.guess()).format();
}

function readCurrentTimestamp(){
    var text_date = readJSON(__dirname + '/public/datasets/current.json')['timestamp'];
    return new Date(convert_time_utc(text_date));
}

function readCurrentSensorTemp(){
    return readJSON(__dirname + '/public/datasets/current.json')['sensor']['temp_f'].toFixed(1);
}

function readCurrentWeatherTemp(){
    return readJSON(__dirname + '/public/datasets/current.json')['weather']['temp_f'].toFixed(1);
}

function readWeatherLocation(){
    return readJSON(__dirname + '/public/datasets/current.json')['weather']['location'];
}

function convert_time_points_utc(json_data) {
    var data = json_data['dataset'];
    var converted_data = [];
    for (var i = 0; i < data.length; i++) {
        var utc_time = convert_time_utc(data[i][0]);
        converted_data[i] = [utc_time, data[i][1], data[i][2]];
    }
    return converted_data;
}

function readAverages(){
    return readJSON(__dirname + '/public/datasets/avgs.json');
}

function read12hrPlot () {
    return convert_time_points_utc(readJSON(__dirname + '/public/datasets/12hr.json'));
}

function read24hrPlot () {
    return convert_time_points_utc(readJSON(__dirname + '/public/datasets/24hr.json'));
}

function read2dPlot () {
    return convert_time_points_utc(readJSON(__dirname + '/public/datasets/2d.json'));
}

function read5dPlot () {
    return convert_time_points_utc(readJSON(__dirname + '/public/datasets/5d.json'));
}

function read10dPlot () {
    return convert_time_points_utc(readJSON(__dirname + '/public/datasets/10d.json'));
}

module.exports.current12hrPlot = read12hrPlot;
module.exports.current24hrPlot = read24hrPlot;
module.exports.current2dPlot = read2dPlot;
module.exports.current5dPlot = read5dPlot;
module.exports.current10dPlot = read10dPlot;
module.exports.currentSensorTemp = readCurrentSensorTemp;
module.exports.currentWeatherTemp = readCurrentWeatherTemp;
module.exports.currentDate = readCurrentTimestamp;
module.exports.weatherLocation = readWeatherLocation;
module.exports.averages = readAverages;

