/*
 * The server component create for Andrea Esposito's Bachelor's Thesis.
 * Copyright (C) 2020  Andrea Esposito <a.esposito39@studenti.uniba.it>
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

import * as fs from "fs";
import * as shortid from "shortid";
import { spawn } from "child_process";

export type FinalData = {
    ui: string; ///< The user ID
    t: number; ///< The timestamp
    u: string; ///< The visited URL
    m: { ///< Various data regarding the mouse
        p: [number, number]; ///< The mouse position.
        b: { ///< The mouse buttons
            l: boolean; ///< Is the left button pressed?
            m: boolean; ///< Is the middle button pressed?
            r: boolean; ///< Is the right button pressed?
            [key: string]: boolean; ///< Are other buttons pressed?
        };
    };
    s: { ///< Various data about the scroll position
        a: [number, number]; ///< The absolute scroll position.
        r: [number, number]; ///< The relative scroll position (from the bottom of the screen).
    };
    w: [number, number]; ///< Various data about the browser's window. w[0] is the width, w[1] is the height.
    k: { ///< An array of keys that's currently pressed
        a: boolean; ///< Is a alphabetic key pressed?
        n: boolean; ///< Is a numeric key pressed?
        s: boolean; ///< Is a symbol key pressed?
        f: boolean; ///< Is a function key pressed?
    };
    e?: { [key: string]: number }; ///< The emotion analysis results
    i?: string; ///< The webcam snapshot as a data URI.
}

/**
 * The data processor.
 *
 * This class processes the collected data, by adding various features (that can
 * be extracted by the existing fields).
 */
export default class DataProcessor {
    /**
     * Get the minimum accepted value for the emotions' fields. If the
     * registered value is less than the returned value, the emotions' object
     * can be safely discarded.
     * 
     * @returns {number} The minimum accepted value.
     * @private
     */
    static get _minimumAcceptedValue(): number {
        return 1;
    }

    /**
     * Round a value to two decimal places.
     * 
     * @param {number} val The value to be rounded.
     * @returns {number} The value rounded to two decimal places.
     * @private
     */
    static _roundValue(val: number): number {
        return Math.round((val + Number.EPSILON) * 100) / 100;
    }

    /**
     * Extract the emotions from the image field.
     *
     * @param {Object} data The data to work on.
     * @returns {Promise<Object[]>} A promise that will be resolved once the
     * analysis is completed. The returned parameter contains the modified data.
     * @private
     */
    static _analyzeEmotions(collectedData): Promise<FinalData[]> {
        const data = new Array<FinalData>();
        collectedData.forEach(e => {
            const newElement: FinalData = {
                i: e.image,
                k: {
                    a: e.keyboard.alpha,
                    f: e.keyboard.function,
                    n: e.keyboard.numeric,
                    s: e.keyboard.symbol
                },
                m: {
                    b: {
                        l: e.mouse.buttons.left,
                        r: e.mouse.buttons.right,
                        m: e.mouse.buttons.middle
                    },
                    p: [e.mouse.position.x, e.mouse.position.y]
                },
                s: {
                    a: [e.scroll.absolute.x, e.scroll.absolute.y],
                    r: [e.scroll.relative.x, e.scroll.absolute.y]
                },
                t: e.timestamp,
                u: e.url,
                ui: e.userId,
                w: [e.window.x, e.window.y]
            };

            Object.keys(e.mouse.buttons).forEach(k => {
                if (k !== "left" && k !== "right" && k !== "middle") {
                    const newKey = k.substr(0, 1) + k.substr(k.length - 1, 1);
                    newElement.m.b[newKey] = e.mouse.buttons[k];
                }
            });
            data.push(newElement);
        });

        return new Promise<FinalData[]>(resolve => {
            const fileName = "temp/" + shortid.generate() + ".temp";
            const file = fs.createWriteStream(fileName);
            data.forEach(e => e.i && file.write(e.i + "\n"));
            file.end();
            console.log("Created temp file: ", fileName);

            try {
                const analysis = spawn(process.env.EMOTIONS_EXECUTABLE, ["--file", fileName], { stdio: ["pipe", "pipe", "pipe"] });
                let out = "";
                analysis.stdout.on("data", (chunk) => out += chunk.toString());
                analysis.on("close", () => {
                    if (out !== "") {
                        const emotions = JSON.parse(out);
                        let j = 0;
                        for (let i = 0; i < data.length; i++) {
                            if (data[i].i) {
                                data[i].e = {};
                                if (emotions[j].emotions) {
                                    Object.entries(emotions[j].emotions).forEach(([key, value]: [string, number]) => {
                                        const newKey = key === "surprise" ? "su" : key.substr(0, 1);
                                        value = DataProcessor._roundValue(value);
                                        if (key === "valence" || key === "engagement" || value >= DataProcessor._minimumAcceptedValue) {
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
     * @param {Object|Object[]} data The data to be processed.
     * @returns {Promise<Object[]>} A promise that will be resolved once all the
     * data have been processed. The promise's parameter holds the modified
     * data.
     */
    static process(data): Promise<FinalData[]> {
        if (!data) return;
        if (!Array.isArray(data)) data = [data];

        return DataProcessor._analyzeEmotions(data);
    }
}
