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

function readCurrentTimestamp(){
    var text_date = readJSON(__dirname + '/public/datasets/current.json')['timestamp'];
    var tz_formatted = moment.tz(text_date, "America/Los_Angeles").format();
    return new Date(tz_formatted);
}

function readCurrentSensorTemp(){
    return readJSON(__dirname + '/public/datasets/current.json')['sensor']['temp_f'].toFixed(1);
}

function readCurrentWeatherTemp(){
    return readJSON(__dirname + '/public/datasets/current.json')['weather']['temp_f'].toFixed(1);
}

function read12hrPlot () {
    return readJSON(__dirname + '/public/datasets/12hr.json');
}

function read24hrPlot () {
    return readJSON(__dirname + '/public/datasets/24hr.json');
}

module.exports.current12hrPlot = read12hrPlot;
module.exports.current24hrPlot = read24hrPlot;
module.exports.currentSensorTemp = readCurrentSensorTemp;
module.exports.currentWeatherTemp = readCurrentWeatherTemp;
module.exports.currentDate = readCurrentTimestamp;

