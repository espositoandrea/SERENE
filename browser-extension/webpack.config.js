const {CheckerPlugin} = require('awesome-typescript-loader');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const {optimize} = require('webpack');
const {join} = require('path');

let prodPlugins = [];
if (process.env.NODE_ENV === 'production') {
    prodPlugins.push(
        new optimize.AggressiveMergingPlugin(),
        new optimize.OccurrenceOrderPlugin()
    );
}

const survey = require("./src/survey/survey-data");

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
        survey: join(__dirname, 'src/survey/survey.js'),
    },
    output: {
        path: join(__dirname, 'dist/survey/'),
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
            filename: 'survey.html',
            template: '!!ejs-loader!src/survey/survey.ejs',
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

const extensionConfig = Object.assign({}, commonConfig, {
    entry: {
        contentscript: join(__dirname, 'src/contentscript/contentscript.ts'),
        background: join(__dirname, 'src/background/background.ts')
    },
    output: {
        path: join(__dirname, 'dist'),
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

module.exports = [extensionConfig, surveyConfig];
