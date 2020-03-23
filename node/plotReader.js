/**
 * Created by MikeGA on 2/13/17.
 */
var fs = require('fs');


function readJSON(filename){
    var contents = fs.readFileSync(filename);
    // Define to JSON type
    return JSON.parse(contents);
}

function readCurrentTimestamp(){
    var text_date = readJSON(__dirname + '/public/datasets/current.json')['timestamp'];
    return new Date(text_date);
}

function readCurrentSensorTempF(){
    return readJSON(__dirname + '/public/datasets/current.json')['sensor']['temp_f'].toFixed(1);
}

function readCurrentSensorTempC(){
    return readJSON(__dirname + '/public/datasets/current.json')['sensor']['temp_c'].toFixed(1);
}

function readCurrentWeatherTemp(){
    return readJSON(__dirname + '/public/datasets/current.json')['weather']['temp_f'].toFixed(1);
}

function readWeatherLocation(){
    return readJSON(__dirname + '/public/datasets/current.json')['weather']['location'];
}

function readAverages(){
    return readJSON(__dirname + '/public/datasets/avgs.json');
}

function read12hrPlot () {
    return readJSON(__dirname + '/public/datasets/12hr.json');
}

function read24hrPlot () {
    return readJSON(__dirname + '/public/datasets/24hr.json');
}

function read2dPlot () {
    return readJSON(__dirname + '/public/datasets/2d.json');
}

function read5dPlot () {
    return readJSON(__dirname + '/public/datasets/5d.json');
}

function read10dPlot () {
    return readJSON(__dirname + '/public/datasets/10d.json');
}

module.exports.current12hrPlot = read12hrPlot;
module.exports.current24hrPlot = read24hrPlot;
module.exports.current2dPlot = read2dPlot;
module.exports.current5dPlot = read5dPlot;
module.exports.current10dPlot = read10dPlot;
module.exports.currentSensorTempF = readCurrentSensorTempF;
module.exports.currentSensorTempC = readCurrentSensorTempC;
module.exports.currentWeatherTempF = readCurrentWeatherTemp;
module.exports.currentDate = readCurrentTimestamp;
module.exports.weatherLocation = readWeatherLocation;
module.exports.averages = readAverages;

