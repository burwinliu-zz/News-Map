import 'ol/ol.css';
import {Map, View} from 'ol';
import 'ol/proj'
import {GeoJSON} from "ol/format";
import TileLayer from 'ol/layer/Tile';
import OSM from 'ol/source/OSM';
import VectorLayer from 'ol/layer/Vector';
import VectorSource from 'ol/source/Vector';


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
                url: '.data',
                format: new GeoJSON(),
            })
        })
    ],
    view: new View({
        center: [0, 0],
        zoom: 2,
    }),
});


// Need to check commit -- computer setup
// Reference code from http://openlayersbook.github.io/ch06-styling-vector-layers/example-07.html
/*
const high = [64,196,64,1];
const mid = [108,152,64,1];
const low = [152,108,64,1];
const poor = [196,32,32,1];
// map the income level codes to a colour value, grouping them
const incomeLevels = {
    'HIC': high, // high income
    'OEC': high, // high income OECD
    'NOC': high, // high income, non-OECD
    'UMC': mid, // upper middle income
    'MIC': mid, // middle income
    'LMC': mid, // lower middle income
    'LIC': low, // low income
    'LMY': low, // low and middle income
    'HPC': poor // heavily indebted poor country
};

// a default style is good practice!
const defaultStyle = new Style({
    fill: new Fill({
      color: [250,250,250,1]
    }),
    stroke: new Stroke({
      color: [220,220,220,1],
      width: 1
    })
});

// a javascript object literal can be used to cache
// previously created styles. Its very important for
// performance to cache styles.
const styleCache = {};

// the style function returns an array of styles
// for the given feature and resolution.
// Return null to hide the feature.
function styleFunction(feature, resolution) {
    // get the incomeLevel from the feature properties
    const level = feature.get('incomeLevel');
    // if there is no level or its one we don't recognize,
    // return the default style (in an array!)
    if (!level || !incomeLevels[level]) {
      return [defaultStyle];
    }
    // check the cache and create a new style for the income
    // level if its not been created before.
    if (!styleCache[level]) {
      styleCache[level] = new Style({
        fill: new Fill({
          color: incomeLevels[level]
        }),
        stroke: defaultStyle.stroke
      });
    }
    // at this point, the style for the current level is in the cache
    // so return it (as an array!)
    return [styleCache[level]];
}

var source = new GeoJSON({
    projection: 'EPSG:3857',
    url: '../assets/data/countries.geojson'
});

var countries = new Vector({
    source: source,
    style: styleFunction
});

var center = transform([0, 0], 'EPSG:4326', 'EPSG:3857');

var view = new View({
    center: center,
    zoom: 1
});

var map = new Map({
    target: 'map',
    layers: [countries],
    view: view
});

// we want to merge the country data with the income level data. After
// the country data is 'ready', we can load the income level data and
// the add a new property by linking the two sets of data on the
// ISO country code that is present in both data sets.
var key = source.on('change', function(event) {
    if (source.getState() == 'ready') {
        source.unByKey(key);
        $.ajax('../assets/data/income_levels.json').done(function(data) {
            countries.getSource().forEachFeature(function(feature) {
                var code = feature.get('iso_a2');
                if (data[code]) {
                    feature.set('incomeLevel', data[code]);
                }
            });
        });
    }
});


const map = new Map({
    target: 'map',
    layers: [countries],
    view: view
});
*/