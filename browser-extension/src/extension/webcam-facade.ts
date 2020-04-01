import * as Webcam from 'webcamjs';

/**
 * A facade singleton object to use the webcam.
 */
export default class WebcamFacade {
    private static isWebcamEnabled: boolean = false;

    public static get isEnabled(): boolean {
        return WebcamFacade.isWebcamEnabled;
    }

    public static enableWebcam() {
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
        Webcam.on('load', () => {
            WebcamFacade.isWebcamEnabled = true;
        });
    }

    /**
     * Get a photo taken with the webcam.
     * @return Promise a promise containing the data string of the taken photo.
     */
    public static async snapPhoto(): Promise<string> {
        return new Promise<string>(resolve => {
            if (WebcamFacade.isWebcamEnabled) {
                Webcam.snap(async data_uri => {
                    resolve(await data_uri);
                });
            }
        });
    }
}
