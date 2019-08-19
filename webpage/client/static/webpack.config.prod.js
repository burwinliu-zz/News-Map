const webpack = require('webpack');
const resolve = require('path').resolve;
const config = {
    entry: __dirname + '/scripts/index.js',
    output:{
        path: resolve('../public'),
        filename: 'bundle.js',
        publicPath: resolve('../public')
    },
    resolve: {
        extensions: ['.js','.css']
    },
};
module.exports = config;