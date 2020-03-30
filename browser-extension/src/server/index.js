const express = require("express");
const bodyParser = require("body-parser");

const app = express();
const port = 3000;
const requestSizeLimit = '50mb';

app.use(bodyParser.json({limit: requestSizeLimit}));
app.use(bodyParser.urlencoded({limit: requestSizeLimit, extended: false}));

app.post("/data/store", async (request, response) => {
    const data = JSON.parse(request.body.data);
    // Data received: notify the sender
    response.send({done: true, errors: null});

    // Analyze the images in a browser (needed by Affdex)
    const puppeteer = require('puppeteer');
    const results = await (async () => {
        const browser = await puppeteer.launch();
        const page = await browser.newPage();
        await page.addScriptTag({path: require.resolve('jquery')});
        await page.addScriptTag({path: require.resolve('lodash')});
        await page.addScriptTag({path: './emotion-analysis/affdex/affdex.js'});
        await page.addScriptTag({path: './emotion-analysis/emotion-analysis.js'});
        page.on('console', msg => console.log('PAGE LOG:', msg.text()));

        const res = await page.evaluate((image) => {
            return window.EmotionAnalysis.analyzePhoto(image);
        }, data.map(e => e.image));
        await browser.close();
        return res;
    })();
    // Save the results in data
    data.forEach((el, index) => el.emotions = results[index]);

    // TODO: Store 'data'
});

app.listen(port, () => {
    console.log(`Listening on port ${port}`);
});
