import * as Webcam from 'webcamjs';

/**
 * A facade singleton object to use the webcam.
 */
export default class WebcamFacade {
    private static instance: WebcamFacade;
    private static isWebcamEnabled: boolean = false;

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
        Webcam.on('load', WebcamFacade.enableWebcam);
    }

    /**
     * Get the instance of the WebcamFacade.
     */
    public static getInstance() {
        if (!WebcamFacade.instance) {
            WebcamFacade.instance = new WebcamFacade();
        }
        return WebcamFacade.instance;
    }

    private static enableWebcam() {
        WebcamFacade.isWebcamEnabled = true;
    }

    /**
     * Get a photo taken with the webcam.
     * @return Promise a promise containing the data string of the taken photo.
     */
    async snapPhoto(): Promise<string> {
        return new Promise<string>(resolve => {
            if (WebcamFacade.isWebcamEnabled) {
                Webcam.snap(async data_uri => {
                    resolve(await data_uri);
                });
            }
        });
    }
}