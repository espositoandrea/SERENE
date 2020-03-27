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

/*
 * This file has been highly modified by its original author (Andrea Esposito),
 * to adapt it to the nature and source code of this project.
 *
 * NOTE: A copy of the original license can be found at
 *         https://github.com/F-S-C/Emotionally.
 */


import * as $ from 'jquery';
import * as _ from 'lodash';
import * as Webcam from 'webcamjs';
import affdex from "./affdex/affdex.js";

export enum FaceMode {
    /** A value to be used if the video has large faces */
    LARGE_FACES = affdex.FaceDetectorMode.LARGE_FACES,
    /** A value to be used if the video has small faces */
    SMALL_FACES = affdex.FaceDetectorMode.SMALL_FACES
}

export interface AnalysisConfiguration {
    start?: number,
    sec_step?: number,
    stop?: number,
    faceMode?: FaceMode,
    detect?: {
        emotions?: boolean,
        expressions?: boolean,
        emojis?: boolean,
        appearance?: boolean
    }
}

export default class EmotionAnalysis {
    private detector;

    private constructor(options?: AnalysisConfiguration) {
        options = _.merge(EmotionAnalysis.getDefaultConfiguration(), options ?? {});

        // Decide whether your video has large or small face
        const faceMode = options.faceMode;

        // Decide which detector to use photo or stream
        this.detector = new affdex.PhotoDetector(faceMode);
        // const detector = new affdex.FrameDetector(faceMode);

        // Initialize Emotion and Expression detectors
        if (options.detect.emotions) this.detector.detectAllEmotions();
        if (options.detect.expressions) this.detector.detectAllExpressions();
        if (options.detect.emojis) this.detector.detectAllEmojis();
        if (options.detect.appearance) this.detector.detectAllAppearance();

        // Initialize detector
        console.log("#logs", "Initializing detector...");
        this.detector.start();

        let webcamHolder = document.createElement('div');
        webcamHolder.id = '__AESPOSITO_EXTENSION__webcam-holder';
        document.body.appendChild(webcamHolder);
        Webcam.set({
            width: 320,
            height: 240,
            image_format: 'jpeg',
            jpeg_quality: 90
        });
        Webcam.attach(webcamHolder.id);
        Webcam.on('load', EmotionAnalysis.enableWebcam);
    }

    private static instance: EmotionAnalysis;

    public static getInstance() {
        if (!EmotionAnalysis.instance) {
            EmotionAnalysis.instance = new EmotionAnalysis();
        }

        return EmotionAnalysis.instance;
    }

    /**
     * Create a new default configuration.
     * @property {number} [start=0] Where to start (in seconds)
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
     */
    static getDefaultConfiguration(): AnalysisConfiguration {
        return {
            start: 0,
            sec_step: 1,
            stop: undefined,
            faceMode: FaceMode.LARGE_FACES,
            detect: {
                emotions: true,
                expressions: true,
                emojis: true,
                appearance: true
            }
        };
    }

    async analyzePhoto(photo: any, photoTimestamp: Date) {
        return new Promise<any>(resolve => {

            let options = EmotionAnalysis.getDefaultConfiguration();

            // Decide whether your video has large or small face
            const faceMode = options.faceMode;

            // Decide which detector to use photo or stream
            this.detector = new affdex.PhotoDetector(faceMode);
            // const detector = new affdex.FrameDetector(faceMode);

            // Initialize Emotion and Expression detectors
            if (options.detect.emotions) this.detector.detectAllEmotions();
            if (options.detect.expressions) this.detector.detectAllExpressions();
            if (options.detect.emojis) this.detector.detectAllEmojis();
            if (options.detect.appearance) this.detector.detectAllAppearance();

            let detection_results = []; // for logging all detection results.

            //Add a callback to notify when the detector is initialized and ready for running.
            this.detector.addEventListener("onInitializeSuccess", function () {
                console.log("#logs", "The detector reports initialized");
                console.log("#logs", "Please upload file(s) to process");
                getNextImage()
            });

            // Load next image.
            function getNextImage() {
                const img = new Image();
                img.onload = imageLoaded;
                img.src = photo;
            }

            let emotionAnalysis = this;

            //Once the image is loaded, pass it down for processing
            function imageLoaded(event) {
                const contxt = document.createElement('canvas').getContext('2d');
                contxt.canvas.width = this.width;
                contxt.canvas.height = this.height;
                contxt.drawImage(this, 0, 0, this.width, this.height);
                // Pass the image to the detector to track emotions
                if (emotionAnalysis.detector && emotionAnalysis.detector.isRunning) {
                    emotionAnalysis.detector.process(contxt.getImageData(0, 0, this.width, this.height), 0);
                }
            }

            this.detector.addEventListener("onImageResultsSuccess", function (faces, image, timestamp) {
                // drawImage(image);
                console.log('#results', "Timestamp: " + timestamp.toFixed(2));
                console.log('#results', "Number of faces found: " + faces.length);
                if (faces.length > 0) {
                    faces[0].emotions.timestamp = photoTimestamp;
                    // Append filename
                    // console.log(file_val)
                    detection_results.push(Object.assign({}, faces[0].emotions, faces[0].expressions));
                } else {
                    detection_results.push({timestamp: photoTimestamp, empty: true})
                    // If face is not detected skip entry.
                    console.log('Cannot find face, skipping entry');
                }
                console.log("EndofDuration");
                resolve(detection_results);
                console.log("#emotions", "All images processed, results will be automatically downloaded.");
            });
        });
    }

    private static isWebcamEnabled: boolean = false;

    private static enableWebcam() {
        EmotionAnalysis.isWebcamEnabled = true;
    }

    async analyzeWebcamPhoto() {
        return new Promise<any>((resolve, reject) => {
            if (EmotionAnalysis.isWebcamEnabled) {
                Webcam.snap(async data_uri => {
                    resolve(await this.analyzePhoto(data_uri, new Date()));
                });
            }
        });
    }
}