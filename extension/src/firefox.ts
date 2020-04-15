import WebcamFacade from "./webcam-facade";

WebcamFacade.enableWebcam();

window.addEventListener('message', function (event) {
    if (event.data.type && event.data.type === "ESPOSITOTHESIS___SNAP_WEBCAM") {
        window.postMessage({type: 'ESPOSITOTHESIS___RETURN_WEBCAM_SNAP', snap: WebcamFacade.snapPhoto()}, '*');
    }
});
