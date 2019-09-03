import {Map, View} from 'ol';
import {fromLonLat} from 'ol/proj'
import {GeoJSON} from "ol/format";
import VectorLayer from 'ol/layer/Vector';
import {Fill, Style} from "ol/style";
import VectorSource from "ol/source/Vector";
/*
    Data for countries.geojson from https://github.com/datasets/geo-countries
        All data is licensed under the Open Data Commons Public Domain Dedication and License.
        Note that the original data from Natural Earth is public domain. While no credit is formally required a link
        back or credit to Natural Earth, Lexman and the Open Knowledge Foundation is much appreciated.
        All source code is licenced under the MIT licence.
*/


/*
    Meant to retrieve data from db
 */
console.log("0.0.2.1.5");
const tableInner = '<tr><th scope="col">Headline</th><th scope="col">URL</th></tr>';
const colours = JSON.parse(a);
let load_in = false;
let opened_side = false;

// Views
const mapView = new View({
    center: fromLonLat([37.41, 8.82]),
    zoom: 4,
    maxZoom: 7,
    minZoom: 2,
});

// Styles
function countryStyle(feature){
    let style;
    if(feature.get("ISO_A2") in colours) {
        style = new Style({
            fill: new Fill({
                color: colours[feature.get("ISO_A2")],
            })
        });
    }
    else{
        // TODO still need to either delete countries that arent showing up on both ends, or just ignoring them -- or unifying?
        //  maybe create own countries database and adding in extra iso codes
        style = new Style({
            fill: new Fill({
                color: 'white',
            })
        });
    }
    return style;
}


// Layers
const countryLayer = new VectorLayer({
    source: new VectorSource({
        format: new GeoJSON(),
        url: "/static/data/countries.geojson"
    }),
    style: countryStyle
});

// Map declaration
const map = new Map({
    target: 'map',
    layers: [
        countryLayer
    ],
    view: mapView
});

map.on('rendercomplete', e => {
    if(!load_in){
        document.getElementById('preloader').classList.toggle('fade');
        document.getElementById('main-page').classList.toggle('show');
        load_in = true;
    }
});

async function update(event){
    map.forEachFeatureAtPixel(event.pixel, async function(feature) {
        // Set vars
        const url_data='/data?iso=' + feature.get("ISO_A2");
        let response_data = await fetch(url_data,);
        let json_data = await response_data.json();
        let key;
        const tableRef = document.getElementById('table');
        const statusDisplay = document.getElementById('status_display');

        const url_name ='/data_country_name?iso=' + feature.get("ISO_A2");
        let response_name = await fetch(url_name,);
        let json_name = await response_name.json();

        // Set name of country
        statusDisplay.innerHTML = json_name['code'];

        tableRef.innerHTML = tableInner;
        for(key in json_data){
            const headline = key;
            const url = json_data[key];
            const newRow   = tableRef.insertRow(tableRef.rows.length);
            const headlineCell = newRow.insertCell(0);
            const urlCell  = newRow.insertCell(1);
            const urlText  = document.createTextNode(url);
            const headlineText  = document.createTextNode(headline);
            urlCell.appendChild(urlText);
            headlineCell.appendChild(headlineText);
        }
        if(!opened_side){
            opened_side = true;
            document.getElementById('sidebar').classList.toggle('active');
        }

    });
}

map.on('click', async function(event) {
    const content = document.getElementById('sidebar-content');
    if (!(content.classList.contains('updating'))) {
        content.classList.toggle('updating');
    }
    await update(event);
    document.getElementById('sidebar-content').classList.toggle('updating');
});

const sleep = (milliseconds) => {
  return new Promise(resolve => setTimeout(resolve, milliseconds))
};