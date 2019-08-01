import 'ol/ol.css';
import {Map, View} from 'ol';
import {fromLonLat} from 'ol/proj'
import {GeoJSON} from "ol/format";
import OSM from 'ol/source/OSM';
import VectorLayer from 'ol/layer/Vector';
import {Tile} from "ol/layer";
import {Style, Fill, Stroke, Circle} from "ol/style";
import VectorSource from "ol/source/Vector";


/*
    TODO: Find a way to access these data-points from local post a npm start (using parcel)

    Data for borders.json retrieved from http://thematicmapping.org/downloads/world_borders.php

    Data for countries.geojson from https://github.com/datasets/geo-countries
        All data is licensed under the Open Data Commons Public Domain Dedication and License.
        Note that the original data from Natural Earth is public domain. While no credit is formally required a link
        back or credit to Natural Earth, Lexman and the Open Knowledge Foundation is much appreciated.
        All source code is licenced under the MIT licence.

    Data for custom.json is from https://github.com/AshKyd/geojson-regions under The Un-license
*/

/*
var map = new Map({
    target: 'map',
    layers: [
      new Tile({
        source: new OSM()
      })
    ],
    view: new View({
      center: fromLonLat([37.41, 8.82]),
      zoom: 4
    })
});
*/

/*
const countryStyle = new Style({
    fill: new Fill({
      color: [203, 194, 185, 1]
    }),
    stroke: new Stroke({
      color: [177, 163, 148, 0.5],
      width: 2,
      lineCap: 'round'
    })
});

const countries = new Vector({
    source: new GeoJSON({
      projection: 'EPSG:3857',
      url: './data/borders.json',
    }),
    style: countryStyle
});
*/


const tile =  new Tile({
    source: new OSM()
});

const mapView = new View({
    center: fromLonLat([37.41, 8.82]),
    zoom: 4
});

const url_loc = 'C:\\Users\\terra\\PycharmProjects\\News-Map\\webpage\\scripts\\data\\custom.json'
const map = new Map({
    target: 'map',
    layers: [
        tile,
        new VectorLayer({
            source: new VectorSource({
                format: new GeoJSON(),
                url: url_loc
            }),
            style: new Style({
                fill: new Fill({
                    color: '#D4AF37',
                })
            })
        })
    ],
    view: mapView
});


const countryLayer = new VectorLayer({
    source: new VectorSource({
        format: new GeoJSON(),
        url: 'C:\\Users\\terra\\PycharmProjects\\News-Map\\webpage\\scripts\\data\\custom.json',
    }),
    projection: map.getView().getProjection(),
    /*
    style: function(feature) {
        return({
            fill: new Fill({
                color: '#000000'
            }),
            stroke: new Stroke({
                color: '#000000',
                width: 2,
                lineCap: 'round'
            })
        })
    }
    */
});

//map.addLayer(countryLayer);