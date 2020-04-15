require('dotenv').config()
const express = require('express');
const expressLayouts = require('express-ejs-layouts')
const bodyParser = require('body-parser');
const sassMiddleware = require('node-sass-middleware');
const path = require('path');
const { MongoClient } = require('mongodb');
const cors = require('cors');

const app = express();
const requestSizeLimit = '50mb';

const fs = require('fs');
if (!fs.existsSync('temp')) {
    console.log('Creating temp/ directory');
    fs.mkdirSync('temp');
}

MongoClient.connect(process.env.DB_HOST, (err, client) => {
    if (err) return console.log(err);
    const db = client.db(process.env.DB_NAME);

    app.use(
        sassMiddleware({
            src: __dirname + '/',
            dest: __dirname + '/',
            debug: true,
        })
    );
    app.use(bodyParser.json({ limit: requestSizeLimit }));
    app.use(bodyParser.urlencoded({ limit: requestSizeLimit, extended: false }));
    app.use(cors());
    app.set('views', path.join(__dirname, 'views'));
    app.set('view engine', 'ejs');
    app.set('layout', 'layouts/layout');
    app.set('layout extractScripts', true);
    app.use(expressLayouts);

    app.use('/assets', express.static(path.join(__dirname, 'assets')));
    app.use('/downloads', express.static(path.join(__dirname, 'downloads')));

    // ROUTES

    app.get('/', (req, res) => res.render('home', { title: 'Home' }));

    app.get('/survey', (req, res) => res.render('survey', { title: 'Survey', survey: require("./survey/survey-data") }));

    app.post("/data/store", async (request, response) => {
        const data = JSON.parse(request.body.data);
        // Data received: notify the sender
        response.send({ done: true, errors: null });

        const DataProcessor = require('./data-processor');
        DataProcessor.process(data)
            .then((data) => {
                db.collection('interactions').insertMany(data, (err, result) => {
                    if (err) {
                        // TODO: There was an error in writing to the DB: handle this error
                        return console.log(err);
                    }

                    console.log('saved to database');
                });
            });
    });

    app.post("/survey/store", (request, response) => {
        let userData = request.body;

        db.collection('users').insertOne(userData, (err, result) => {
            if (err) {
                // TODO: There was an error in writing to the DB: handle this error
                response.json({ done: false, errors: err });
                return console.log(err);
            }

            response.json({ done: true, errors: [], userId: result.insertedId });
        });
    });

    app.listen(process.env.PORT, () => {
        console.log(`Listening on port ${process.env.PORT}`);
    });
});
