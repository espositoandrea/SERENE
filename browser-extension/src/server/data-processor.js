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
            const { spawnSync } = require('child_process');
            let analysis = spawnSync(process.env.EMOTIONS_EXECUTABLE, data.filter(e => e).map(e => e.image));
            let emotions = JSON.parse(analysis.stdout.toString());
            let i = 0;
            data.forEach(e => {
                if(e.image) {
                    e.emotions = emotions[i];
                    i++;
                }

                // DELETING THE IMAGE
                delete e.image;
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
    static process(data) {
        if (!data) return;
        if (!Array.isArray(data)) data = [data];

        DataProcessor._analyzeEmotions(data);
    }
}

module.exports = DataProcessor;
