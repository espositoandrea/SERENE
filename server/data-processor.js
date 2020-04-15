/**
 * The data processor.
 *
 * This class processes the collected data, by adding various features (that can
 * be extracted by the existing fields).
 */
class DataProcessor {
    static get _minimumAcceptedValue() {
        return 1;
    }

    static _roundValue(val) {
        return Math.round((val + Number.EPSILON) * 100) / 100;
    }

    /**
     * Extract the emotions from the image field.
     *
     * @param {Object} data The data to work on.
     */
    static _analyzeEmotions(data) {
        return new Promise(resolve => {
            const shortid = require('shortid');
            const fs = require('fs');
            const fileName = 'temp/' + shortid.generate() + '.temp';
            const file = fs.createWriteStream(fileName);
            data.forEach(e => e.i && file.write(e.i + '\n'));
            file.end();

            try {
                const {spawn} = require('child_process');
                let analysis = spawn(process.env.EMOTIONS_EXECUTABLE, ['--file', fileName], {stdio: ['pipe', 'pipe', 'ignore']});
                let out = '';
                analysis.stdout.on('data', (chunk) => out += chunk.toString());
                analysis.on("close", code => {
                    if (out !== "") {
                        let emotions = JSON.parse(out);
                        let j = 0;
                        for (let i = 0; i < data.length; i++) {
                            if (data[i].i) {
                                data[i].e = {};
                                if (emotions[j].emotions) {
                                    Object.entries(emotions[j].emotions).forEach(([key, value]) => {
                                        let newKey = key === "surprise" ? "su" : key.substr(0, 1);
                                        value = DataProcessor._roundValue(value);
                                        if (key === "valence" || key === "engagement" || value>= DataProcessor._minimumAcceptedValue) {
                                            data[i].e[newKey] = value;
                                        }
                                    });
                                }
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
                        delete e.i;
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
                    delete e.i;
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
