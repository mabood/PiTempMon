/**
 * Created by MikeGA on 2/13/17.
 */
var fs = require('fs');


function readJSON(filename){
    var contents = fs.readFileSync(filename);
    // Define to JSON type
    return JSON.parse(contents);
}

function readCurrentSensorTemp(){
    return readJSON(__dirname + '/datasets/current.json')['sensor']['temp_f'].toFixed(1);
}

function readCurrentWeatherTemp(){
    return readJSON(__dirname + '/datasets/current.json')['weather']['temp_f'].toFixed(1);
}

module.exports.read12hrPlot = readJSON(__dirname + 'datasets/12hr.json');
module.exports.read24hrPlot = readJSON(__dirname + 'datasets/24hr.json');

module.exports.currentSensorTemp = readCurrentSensorTemp();
module.exports.currentWeatherTemp = readCurrentWeatherTemp();

