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
    private constructor() {
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
            sec_step: 0.1,
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

    async analyzePhoto(photo: any, options?: AnalysisConfiguration) {
        options = _.assign({}, EmotionAnalysis.getDefaultConfiguration(), options ?? {});
        console.log(photo);
    }

    private static isWebcamEnabled: boolean = false;

    private static enableWebcam() {
        EmotionAnalysis.isWebcamEnabled = true;
    }

    async analyzeWebcamPhoto(options?: AnalysisConfiguration) {
        return new Promise<any>((resolve, reject) => {
            if (EmotionAnalysis.isWebcamEnabled) {
                Webcam.snap(data_uri => {
                    resolve(this.analyzePhoto(data_uri, options));
                });
            }
        });
    }
}