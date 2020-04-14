/*
 * This file is part of Emotionally.
 *
 * Emotionally is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * Emotionally is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with Emotionally.  If not, see <http://www.gnu.org/licenses/>.
 */

"use strict";

// const $ = require('jquery');
// const _ = require('lodash');

/**
 * The interface to the emotion analysis's engine.
 */
class EmotionAnalysis {
    constructor() {
    }

    /**
     * A collection of possible face modes.
     * @typedef {number} FaceMode
     * @enum {number}
     * @readonly
     */
    static get FaceMode() {
        return {
            /** A value to be used if the video has large faces */
            LARGE_FACES: affdex.FaceDetectorMode.LARGE_FACES,
            /** A value to be used if the video has small faces */
            SMALL_FACES: affdex.FaceDetectorMode.SMALL_FACES
        };
    }

    /**
     * Create a new default configuration.
     * @typedef {Object} Configuration
     * @property {number} [start=0] Where to start (in seconds)
     * @property {boolean} [verbose=false] Where to print verbosely
     * @property {number} [sec_step=0.1] The step size of extracting emotion (in
     * seconds).
     * @property {number} [stop=undefined] Where to stop (in seconds). If
     * undefined or less or equal to secs, the entire video will be analyzed.
     * @property {FaceMode} [faceMode=FaceMode.LARGE_FACES] The type of faces in the video.
     * @property {Object} detect
     * @property {boolean} detect.emotions Should it detect emotions?
     * @property {boolean} detect.expressions Should it detect expressions?
     * @property {boolean} detect.emojis Should it detect emojis?
     * @property {boolean} detect.appearance Should it detect appearance?
     * @return {Configuration} The default configuration
     */
    static getDefaultConfiguration() {
        return {
            start: 0,
            sec_step: 1,
            verbose: false,
            stop: undefined,
            faceMode: EmotionAnalysis.FaceMode.LARGE_FACES,
            detect: {
                emotions: true,
                expressions: true,
                emojis: true,
                appearance: true
            }
        };
    }

    /**
     * A callback to be used at the end of an analysis.
     * @callback AnalysisCompletedCallback
     * @param report {string} The generated report.
     */


    /**
     * Analyze a series of photos.
     * @param photo {string[]|string} The photos as data URI.
     * @param {Configuration} [options] The configuration of the analysis.
     */
    static analyzePhoto(photo, options = undefined) {
        return new Promise(resolve => {
            // Set verbose = true to print images and detection succes, false if you don't want info
            if (options === undefined) {
                options = EmotionAnalysis.getDefaultConfiguration();
            } else {
                options = _.assign({}, EmotionAnalysis.getDefaultConfiguration(), options);
            }

            const verbose = false;
            let secs = options.start;
            let sec_step = options.sec_step;
            let stop_sec = options.stop;

            // Decide whether your video has large or small face
            const faceMode = options.faceMode;

            // Decide which detector to use photo or stream
            // var detector = new affdex.PhotoDetector(faceMode);
            const detector = new affdex.PhotoDetector(faceMode);

            // Initialize Emotion and Expression detectors
            if (options.detect.emotions) detector.detectAllEmotions();
            if (options.detect.expressions) detector.detectAllExpressions();
            if (options.detect.emojis) detector.detectAllEmojis();
            if (options.detect.appearance) detector.detectAllAppearance();

            // Init variable to save results
            let detection_results = []; // for logging all detection results.
            if (typeof stop_sec === 'undefined' || stop_sec <= secs) {
                stop_sec = Infinity
            }

            // set fileList as global var
            let fileList;
            // set file as global var
            let file;

            // determines how long the file list is
            let duration;

            // Init variable to save results
            let fileNo = 0;
            let clicks = 0;

            // Initialize detector
            log("#logs", "Initializing detector...");
            detector.start();

            //Add a callback to notify when the detector is initialized and ready for running.
            detector.addEventListener("onInitializeSuccess", function () {
                log("#logs", "The detector reports initialized");
                $("#input").css("visibility", "visible");
                log("#logs", "Please upload file(s) to process");
                loadFile();
            });

            //Load the selected image
            function loadFile(event) {
                $('#results').html("");
                fileList = Array.isArray(photo) ? photo : [photo]; // Load list of files.
                duration = fileList.length;
                log('#logs', 'Loading ' + duration + ' files');
                getNextImage(secs)
            }

            // Load next image.
            function getNextImage(file_idx) {
                // var fileList = document.getElementById('input').files
                file = fileList[file_idx];
                // console.log(file)
                const img = new Image();
                img.onload = imageLoaded;
                img.src = file;
            }

            //Once the image is loaded, pass it down for processing
            function imageLoaded(event) {
                const contxt = document.createElement('canvas').getContext('2d');
                contxt.canvas.width = this.width;
                contxt.canvas.height = this.height;
                contxt.drawImage(this, 0, 0, this.width, this.height);
                // Pass the image to the detector to track emotions
                if (detector && detector.isRunning) {
                    detector.process(contxt.getImageData(0, 0, this.width, this.height), 0);
                }
            }

            detector.addEventListener("onImageResultsSuccess", function (faces, image, timestamp) {
                // drawImage(image);
                $('#results').html("");
                const time_key = "Timestamp";
                const time_val = timestamp;
                const file_key = "FileName";
                const file_val = file.name;
                log('#results', "Timestamp: " + timestamp.toFixed(2));
                log('#results', "Number of faces found: " + faces.length);
                if (verbose) {
                    log("#logs", "Number of faces found: " + faces.length);
                    log("#logs", "Image processed: " + file.name);
                }
                let results = {};
                if (faces.length > 0) {
                    clicks += 1;
                    // Append timestamp
                    faces[0].emotions[time_key] = time_val;
                    // Append filename
                    // console.log(file_val)
                    faces[0].emotions[file_key] = file_val;
                    // Save both emotions and expressions
                    if (options.detect.emotions) results.emotions = faces[0].emotions;
                    if (options.detect.expressions) results.expressions = faces[0].expressions;
                    if (options.detect.emojis) results.emojis = faces[0].emojis;
                    if (options.detect.appearance) results.appearance = faces[0].appearance;
                } else {
                    // If face is not detected skip entry.
                    log('#errors', 'Cannot find face, skipping entry');
                }
                detection_results.push(results);
                if (duration - 1 > secs) {
                    secs = secs + sec_step;
                    getNextImage(secs);
                    // If data accumulated for more than 50,000 timepoints, save data, keep going
                    // if (clicks === 50000) {
                    //     // save and download file
                    //     saveBlob(detection_results, fileNo);
                    //     // increment counter
                    //     fileNo += 1;
                    //     clicks = 0;
                    //     // reset detection results
                    //     detection_results = [];
                    // }
                } else {
                    console.log("EndofDuration");
                    saveBlob(detection_results, fileNo);
                    log("#logs", "All images processed, results will be automatically downloaded.");
                }
            });

            function saveBlob(results, fileNo) {
                resolve(results);
                // var blob = new Blob([results], {type: "application/json"});
                // var saveAs = window.saveAs;
                // saveAs(blob, filename);
            }

            function log(node_name, msg) {
                console.log('EMOTIONS' + node_name + ': ' + msg);
            }
        });
    }
}

// module.exports.default = EmotionAnalysis;
window.EmotionAnalysis = EmotionAnalysis;
// exports.default = EmotionAnalysis;
// export default EmotionAnalysis;
