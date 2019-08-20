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
    module:{
        rules:[
            {
                test:/\.css$/i,
                use:['style-loader','css-loader']
            }
       ]
    },
};
module.exports = config;