const path = require('path');
const {VueLoaderPlugin} = require('vue-loader')
const glob = require('glob');
// const entries = {};
const IGNORE_PATHS = ['unused'];

// glob.sync('./index.js').forEach(pathEntry => {
//     const chunk = pathEntry.split('./views/')[1].split('/main.js')[0];
//     if (IGNORE_PATHS.every(ignorePath => !chunk.includes(ignorePath))) {
//         if (!chunk.includes('/')) {
//             entries[chunk] = pathEntry;
//         }
//         else {
//             const joinChunk = chunk.split('/').join('-');
//             console.log(pathEntry);
//             entries[joinChunk] = pathEntry;
//         }
//     }
// });

// we need export an object. In this object, we define the loaders inside the module.rules.
// when define loader, we need to tell the file type and the loader to use.
// to tell the file type, we use the test property. Webpack will match each pathEntry of files that match with regex value of test.
// in this case, it matchs any string ending with .vue

// vue-loader comes up with plugin. In a .vue file we can write both JS and CSS. This plugin ensures the Webpack rules specified for JS, CSS files are applied to that inside .vue files
let exportObject = {
    // entry: entries,
    entry: './index.js',
    output: {
        path: path.resolve(__dirname, '../app/static/js'),
        filename: '[name].bundle.js'
    },
    module: {
        rules: [
            {
                test: /\.vue$/,
                loader: 'vue-loader'
            },
            {
                test: /\.css$/,
                use: [
                    'vue-style-loader',
                    'css-loader'
                ]
            }
        ]
    },
    plugins: [
        new VueLoaderPlugin()
    ]
}
exportObject.devtool = 'eval-source-map';
module.exports = exportObject;