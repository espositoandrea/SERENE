const { CheckerPlugin } = require('awesome-typescript-loader');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const FixStyleOnlyEntriesPlugin = require("webpack-fix-style-only-entries");
const HtmlWebpackPlugin = require('html-webpack-plugin');
const CopyPlugin = require('copy-webpack-plugin');
const { optimize } = require('webpack');
const { join } = require('path');
const { readFileSync } = require('fs');
const { template } = require('lodash');

let prodPlugins = [];
let isProduction = false;
if (process.env.NODE_ENV === 'production') {
    isProduction = true;
    prodPlugins.push(
        new optimize.AggressiveMergingPlugin(),
        new optimize.OccurrenceOrderPlugin()
    );
}

function ejsViewConfiguration(viewPath, data = {}, layout = 'src/views/layouts/layout.ejs') {
    return {
        minimize: isProduction,
        base: isProduction ? 'https://giuseppe-desolda.ddns.net:8080/' : '.',
        inject: false,
        template: layout,
        templateParameters: {
            body: template(readFileSync(viewPath))(data)
        }
    }
}

module.exports = {
    mode: process.env.NODE_ENV,
    devtool: isProduction ? 'source-map' : 'inline-source-map',
    target: 'node',
    node: {
        __dirname: true
    },
    plugins: [
        new FixStyleOnlyEntriesPlugin(),
        new CheckerPlugin(),
        ...prodPlugins,
        new CopyPlugin([
            { from: 'src/assets/images/', to: 'assets/images/' },
            { from: 'src/.env.example', to: '.env', toType: 'file' }
        ]),
        new HtmlWebpackPlugin({
            filename: 'survey.html',
            title: 'Survey',
            ...ejsViewConfiguration('src/views/survey.ejs', { survey: require('./src/survey-data.js') })
        }),
        new HtmlWebpackPlugin({
            filename: 'index.html',
            title: 'Home',
            ...ejsViewConfiguration('src/views/home.ejs')
        }),
        new MiniCssExtractPlugin({
            filename: 'assets/style/[name].css',
            chunkFilename: 'assets/style/[id].css',
        })
    ],
    entry: {
        index: join(__dirname, 'src/server.ts'),
        style: join(__dirname, 'src/assets/style/style.scss'),
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
                test: /\.s(a|c)ss$/,
                use: [
                    MiniCssExtractPlugin.loader,
                    'css-loader',
                    {
                        loader: 'sass-loader',
                        options: {
                            sourceMap: !isProduction
                        }
                    }
                ]
            },
        ],
    },
    resolve: {
        extensions: ['.ts', '.js', '.scss'],
    },
};
