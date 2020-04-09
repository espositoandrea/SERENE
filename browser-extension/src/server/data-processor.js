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
            const { spawn } = require('child_process');
            data.forEach((el, index) => {
                if (el.image) {
                    let analysis = spawn(process.env.EMOTIONS_EXECUTABLE, ['-i', el.image]);
                    analysis.stdout.on('data', data => {
                        // Save the results in data
                        el.emotions = JSON.parse(data);
                    });
                }
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
