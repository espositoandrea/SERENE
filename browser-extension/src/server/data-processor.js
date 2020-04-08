/**
 * The data processor.
 *
 * This class processes the collected data, by adding various features (that can
 * be extracted by the existing fields). 
 */
class DataProcessor {
    /**
     * Extract the emotions from the image field.
     * 
     * @param {Object} data The data to work on.
     */
    static _analyzeEmotions(data) {
        try {
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
        } catch (e) {
            // TODO: Analysis error. Handle this error.
            console.error("Analysis error", e);
        }
    }

    /**
     * Process the data. This modify the passed data injecting various features
     * in them.
     *
     * @param {Object|Array} data The data to be processed.
     */
    static process(data){
        if(!data) return;
        if(!Array.isArray(data)) data = [data];

        // DataProcessor._analyzeEmotions(data);
    }
}

module.exports.default = DataProcessor;
