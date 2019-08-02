import 'ol/ol.css';
import {Map, View} from 'ol';
import {fromLonLat} from 'ol/proj'
import {GeoJSON} from "ol/format";
import OSM from 'ol/source/OSM';
import VectorLayer from 'ol/layer/Vector';
import {Tile} from "ol/layer";
import {Style, Fill, Stroke, Circle} from "ol/style";
import VectorSource from "ol/source/Vector";
import * as $ from "jquery"


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

const mapView = new View({
    center: fromLonLat([37.41, 8.82]),
    zoom: 4
});

const countryStyle = new Style({
    fill: new Fill({
        color: '#D4AF37',
    })
});

const countryColours = new VectorLayer({
    source: new VectorSource({
        format: new GeoJSON(),
        //Temporary fix by using github raw data
        // TODO: Make a new solution with local access of json file (see getJSON from jquery?)
        url: "https://raw.githubusercontent.com/burwinliu/News-Map/master/webpage/scripts/data/countries.geojson",
    }),
    style: countryStyle,
});

const tile =  new Tile({
    source: new OSM(),
    style: countryStyle,
});

const map = new Map({
    target: 'map',
    layers: [
        tile,
        countryColours
    ],
    view: mapView,
    style: countryStyle
});
