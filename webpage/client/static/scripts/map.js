import 'ol/ol.css'
import {Map, View} from 'ol';
import {fromLonLat} from 'ol/proj'
import {GeoJSON} from "ol/format";
import VectorLayer from 'ol/layer/Vector';
import {Style, Fill} from "ol/style";
import VectorSource from "ol/source/Vector";
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
console.log("0,0.1.2")
// Views
const mapView = new View({
    center: fromLonLat([37.41, 8.82]),
    zoom: 4
});

// Styles

async function makeCountryStyle(feature){
    console.log("loading", feature.get("ISO_A2"));
    const response = await fetch('/colours/colours.json');
    const data = await response.json();
    const to_return = new Style({
        fill: new Fill({
            color: data[feature.get("ISO_A2")],
        })
    });
    console.log(to_return);
    console.log("DATA", data);
    return to_return
}


// Layers
const countryLayer = new VectorLayer({
    source: new VectorSource({
        format: new GeoJSON(),
        // Temporary fix by using github raw data
        // TODO: Make a new solution with local access of json file (see getJSON from jquery?)
        // TODO: Serve up this geojson on the site server (APACHE SERVER)

        url: "/static/data/countries.geojson"
    }),
    style: makeCountryStyle
});

// Map declaration
const map = new Map({
    target: 'map',
    layers: [
        countryLayer
    ],
    view: mapView
});
