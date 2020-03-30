const {CheckerPlugin} = require('awesome-typescript-loader');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const nodeExternals = require('webpack-node-externals');
const {optimize} = require('webpack');
const {join} = require('path');

let prodPlugins = [];
if (process.env.NODE_ENV === 'production') {
    prodPlugins.push(
        new optimize.AggressiveMergingPlugin(),
        new optimize.OccurrenceOrderPlugin()
    );
}

const survey = require("./survey/survey-data");

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

const surveyConfig = Object.assign({}, commonConfig, {
    entry: {
        survey: join(__dirname, 'survey/survey.js'),
    },
    output: {
        path: join(__dirname, '../../dist/server/survey/'),
        filename: '[name].js',
    },
    module: {
        rules: [
            {
                test: /\.ejs$/,
                use: ['html-loader', 'ejs-loader']
            },
            {
                test: /\.s[ac]ss$/,
                use: [MiniCssExtractPlugin.loader, 'css-loader', 'sass-loader'],
            }
        ],
    },
    plugins: [
        new HtmlWebpackPlugin({
            filename: 'index.html',
            template: '!!ejs-loader!survey/survey.ejs',
            survey: survey,
            inject: false,
        }),
        new CheckerPlugin(),
        ...prodPlugins,
        new MiniCssExtractPlugin({
            filename: '[name].css',
            chunkFilename: '[id].css',
        }),
    ]
});

module.exports = surveyConfig;
