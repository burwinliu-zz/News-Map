import 'ol/ol.css';
import {Map, View} from 'ol';
import {fromLonLat} from 'ol/proj'
import {GeoJSON} from "ol/format";
import VectorLayer from 'ol/layer/Vector';
import {Style, Fill, Stroke, Circle} from "ol/style";
import VectorSource from "ol/source/Vector";
import * as $ from "jquery"



/*
    TODO on 8/8 -- finish up retrieving data from databases and work on parsing data to colours
    Data for countries.geojson from https://github.com/datasets/geo-countries
        All data is licensed under the Open Data Commons Public Domain Dedication and License.
        Note that the original data from Natural Earth is public domain. While no credit is formally required a link
        back or credit to Natural Earth, Lexman and the Open Knowledge Foundation is much appreciated.
        All source code is licenced under the MIT licence.

    Data for custom.json is from https://github.com/AshKyd/geojson-regions under The Un-license
*/


/*
    Meant to retrieve data from db
 */




// File serving/loading
$.getJSON("./data/countries.geojson", function(json) {
    console.log(json); // this will show the info it in firebug console
});

// Views
const mapView = new View({
    center: fromLonLat([37.41, 8.82]),
    zoom: 4
});

// Styles
const countryStyle = new Style({
    fill: new Fill({
        color: '#D4AF37',
    })
});

const englandStyle = new Style({
    fill: new Fill({
        color: '#000000',
    })
});

// Layers
const countryColours = new VectorLayer({
    source: new VectorSource({
        format: new GeoJSON(),
        // Temporary fix by using github raw data
        // TODO: Make a new solution with local access of json file (see getJSON from jquery?)
        // TODO: Serve up this geojson on the site server (APACHE SERVER)

        url: "https://raw.githubusercontent.com/burwinliu/News-Map/master/webpage/scripts/data/countries.geojson",
    }),
    style: function(feature){
        if(feature.get("ADMIN") === "United Kingdom"){
            return englandStyle;
        }
        else{
            return countryStyle;
        }

    },
});

// Map declaration
const map = new Map({
    target: 'map',
    layers: [
        countryColours
    ],
    view: mapView,
    style: countryStyle
});
