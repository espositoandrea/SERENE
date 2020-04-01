const express = require("express");
const bodyParser = require("body-parser");
const sassMiddleware = require('node-sass-middleware');
const path = require('path');
const { MongoClient } = require('mongodb');

const app = express();
const port = 3000;
const requestSizeLimit = '50mb';
const databaseConfiguration = {
    name: 'esposito-thesis',
    url: `mongodb+srv://testingUser:ThisIsNotASecurePassword@testingcluster-st6tg.mongodb.net/test?retryWrites=true&w=majority`
};

MongoClient.connect(databaseConfiguration.url, (err, client) => {
    if (err) return console.log(err);
    const db = client.db(databaseConfiguration.name);

    app.use(
        sassMiddleware({
            src: __dirname + '/survey',
            dest: __dirname + '/survey',
            debug: true,
        })
    );
    app.use(bodyParser.json({ limit: requestSizeLimit }));
    app.use(bodyParser.urlencoded({ limit: requestSizeLimit, extended: false }));
    app.set('view engine', 'ejs');
    app.set('views', __dirname);

    const survey = require("./survey/survey-data");
    app.get('/', (req, res) => res.render('survey/survey', { survey }));

    app.use('/survey/', express.static(path.join(__dirname, 'survey')));

    app.post("/data/store", async (request, response) => {
        const data = JSON.parse(request.body.data);
        // Data received: notify the sender
        response.send({ done: true, errors: null });

        // Analyze the images in a browser (needed by Affdex)
        const puppeteer = require('puppeteer');
        const results = await (async () => {
            const browser = await puppeteer.launch();
            const page = await browser.newPage();
            await page.addScriptTag({ path: require.resolve('jquery') });
            await page.addScriptTag({ path: require.resolve('lodash') });
            await page.addScriptTag({ path: './emotion-analysis/affdex/affdex.js' });
            await page.addScriptTag({ path: './emotion-analysis/emotion-analysis.js' });
            page.on('console', msg => console.log('PAGE LOG:', msg.text()));

            const res = await page.evaluate((image) => {
                return window.EmotionAnalysis.analyzePhoto(image);
            }, data.map(e => e.image).filter(e => e));
            await browser.close();
            return res;
        })();
        // Save the results in data
        data.forEach((el, index) => {
            if (el.image) el.emotions = results[index];
        });

        // TODO: Store 'data'
        db.collection('interactions').insertMany(data, (err, result) => {
            if (err) {
                // TODO: There was an error in writing to the DB: handle this error
                return console.log(err);
            }

            console.log('saved to database');
        });
    });

    app.get("/survey/store", (request, response) => {
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
