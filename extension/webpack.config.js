const {CheckerPlugin} = require('awesome-typescript-loader');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const nodeExternals = require('webpack-node-externals');
const {optimize} = require('webpack');
const {join} = require('path');

process.env.NODE_ENV = 'development';

let prodPlugins = [];
if (process.env.NODE_ENV === 'production') {
    prodPlugins.push(
        new optimize.AggressiveMergingPlugin(),
        new optimize.OccurrenceOrderPlugin()
    );
}

const commonConfig = {
    mode: process.env.NODE_ENV,
    devtool: 'inline-source-map',
    plugins: [
        new CheckerPlugin(),
        ...prodPlugins,
        new MiniCssExtractPlugin({
            filename: '[name].css',
            chunkFilename: '[id].css',
        }),
    ],
};

const extensionConfig = Object.assign({}, commonConfig, {
    entry: {
        contentscript: join(__dirname, 'src/contentscript.ts'),
        background: join(__dirname, 'src/background.ts'),
        firefox: join(__dirname, 'src/firefox.ts'),
    },
    output: {
        path: join(__dirname, 'dist/'),
        filename: '[name].js',
    },
    module: {
        rules: [
            {
                exclude: /node_modules/,
                test: /\.ts?$/,
                use: 'awesome-typescript-loader?{configFileName: "tsconfig.json"}',
            },
            {
                test: /\.s[ac]ss$/,
                use: [MiniCssExtractPlugin.loader, 'css-loader', 'sass-loader'],
            }
        ],
    },
    resolve: {
        extensions: ['.ts', '.js'],
    },
});

module.exports = [extensionConfig];
