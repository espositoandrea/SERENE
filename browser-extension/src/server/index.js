require('dotenv').config()
const express = require("express");
const bodyParser = require("body-parser");
const sassMiddleware = require('node-sass-middleware');
const path = require('path');
const { MongoClient } = require('mongodb');

const app = express();
const port = 1880;
const requestSizeLimit = '50mb';

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
    app.set('view engine', 'ejs');
    app.set('views', __dirname);

    const survey = require("./survey/survey-data");
    app.use('/survey/', express.static(path.join(__dirname, 'survey')));
    app.get('/survey', (req, res) => res.render('survey/survey', { survey }));

    app.post("/data/store", async (request, response) => {
        const data = JSON.parse(request.body.data);
        // Data received: notify the sender
        response.send({ done: true, errors: null });

        const DataProcessor = require('./data-processor');
        DataProcessor.process(data);

        db.collection('interactions').insertMany(data, (err, result) => {
            if (err) {
                // TODO: There was an error in writing to the DB: handle this error
                return console.log(err);
            }

            console.log('saved to database');
        });
    });

    app.post("/survey/store", (request, response) => {
        let userData = request.query;

        db.collection('users').insertOne(userData, (err, result) => {
            if (err) {
                // TODO: There was an error in writing to the DB: handle this error
                response.json({ done: false, errors: err });
                return console.log(err);
            }

            response.json({ done: true, errors: [], userId: result.insertedId });
        });
    });

    app.listen(port, () => {
        console.log(`Listening on port ${port}`);
    });
});
