/*
 * The browser extension created for Andrea Esposito's Bachelor's Thesis.
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

import * as Webcam from "webcamjs";

/**
 * A facade singleton object to use the webcam.
 */
export default class WebcamFacade {
    private static isWebcamEnabled = false;
    private static readonly WEBCAM_CONTAINER_ID = "__AESPOSITO_EXTENSION__webcam-holder";

    public static get isEnabled(): boolean {
        return WebcamFacade.isWebcamEnabled;
    }

    public static enableWebcam(): void {
        if(WebcamFacade.isWebcamEnabled) return;

        let webcamHolder = document.getElementById(WebcamFacade.WEBCAM_CONTAINER_ID);
        if (!webcamHolder) {
            webcamHolder = document.createElement("div");
            webcamHolder.id = WebcamFacade.WEBCAM_CONTAINER_ID;
            document.body.appendChild(webcamHolder);
        }

        /* eslint-disable */
        Webcam.set({
            width: 320,
            height: 240,
            image_format: "jpeg",
            jpeg_quality: 90
        });
        /* eslint-enable */

        Webcam.attach(webcamHolder.id);
        Webcam.on("load", () => {
            WebcamFacade.isWebcamEnabled = true;
        });
    }

    public static stopWebcam(): void {
        if(!WebcamFacade.isWebcamEnabled) return;

        Webcam.reset();
        const webcamHolder = document.getElementById(WebcamFacade.WEBCAM_CONTAINER_ID);
        webcamHolder.innerHTML = "";
        WebcamFacade.isWebcamEnabled = false;
    }

    /**
     * Get a photo taken with the webcam.
     * @return Promise a promise containing the data string of the taken photo.
     */
    public static async snapPhoto(): Promise<string> {
        return new Promise<string>(resolve => {
            if (WebcamFacade.isWebcamEnabled) {
                Webcam.snap(async dataUri => {
                    resolve(await dataUri);
                });
            }
        });
    }
}
