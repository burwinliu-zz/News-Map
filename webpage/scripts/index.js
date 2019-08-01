import 'ol/ol.css';
import {Map, View} from 'ol';
import 'ol/proj'
import {GeoJSON} from "ol/format";
import TileLayer from 'ol/layer/Tile';
import OSM from 'ol/source/OSM';
import VectorLayer from 'ol/layer/Vector';
import {Style, Fill, Stroke} from "ol/style";
import VectorSource from "ol/source/Vector";


/*
    Data for borders.json retrieved from http://thematicmapping.org/downloads/world_borders.php
*/


const _myStroke = new Stroke({
   color : '#FFFF00',
   width : 1
});

const _myFill = new Fill({
   color: '#FFFF00'
});

const myStyle = new Style({
   stroke : _myStroke,
   fill : _myFill
 });


new Map({
    target: 'map',
    layers: [
        new TileLayer({
            source: new OSM(),
        }),
        // New VectorLayer with VectorSource and the countries.geojson file as source
        new VectorLayer({
            source: new VectorSource({
                // Trying to look for better solution to find the countries borders -- looking at
                // http://thematicmapping.org/downloads/world_borders.php
                url: './data/borders.json',
                format: new GeoJSON(),
            }),
            style: myStyle,
        }),
    ],
    view: new View({
        center: [0, 0],
        zoom: 2,
    }),
    style: new Style({
        stroke: new Stroke({
            color: '#f00',
            width: 1
        }),
        fill: new Fill({
            color: 'rgba(255,0,0,0.1)'
        })
    })
});
