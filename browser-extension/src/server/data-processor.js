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
        return new Promise(resolve => {
            const shortid = require('shortid');
            const fs = require('fs');
            const fileName = shortid.generate() + '.temp';
            const file = fs.createWriteStream(fileName);
            data.forEach(e => e.image && file.write(e.image + '\n'));
            file.end();
            try {
                const { spawn } = require('child_process');
                let analysis = spawn(process.env.EMOTIONS_EXECUTABLE, ['--file', fileName]);
                let out = '';
                analysis.stdout.on('data', (chunk) => out += chunk.toString());
                analysis.on("close", code => {
                    if (out !== "") {
                        let emotions = JSON.parse(out);
                        let j = 0;
                        for (let i = 0; i < data.length; i++) {
                            if (data[i].image) {
                                data[i].emotions = emotions[j].emotions || {};
                                j++;
                            }
                        }
                    }
                    fs.unlink(fileName, err => {
                        if (err) console.error(err);
                        else console.log("Deleted temp file: ", fileName);
                    });
                    data.forEach(e => {
                        // DELETING THE IMAGE
                        delete e.image;
                    });

                    resolve(data);
                });
            } catch (e) {
                // TODO: Analysis error. Handle this error.
                console.error("Analysis error", e);
                fs.unlink(fileName, err => {
                    if (err) console.error(err);
                    else console.log("Deleted temp file: ", fileName);
                });
                data.forEach(e => {
                    // DELETING THE IMAGE
                    delete e.image;
                });
                resolve(data);
            }
        });
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

        return DataProcessor._analyzeEmotions(data);
    }
}

module.exports = DataProcessor;
