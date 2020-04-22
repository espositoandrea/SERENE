import { ScreenCoordinates, Message, RawData } from './common-types';
import WebcamFacade from './webcam-facade';

export default class ContentScript {
    private static readonly keyboard: Set<string> = new Set<string>();
    private static readonly mousePosition: RawData['mouse']['position'] = new ScreenCoordinates();
    private static readonly mouseButtons: Set<number> = new Set<number>();
    private static takeWebcamPhoto: boolean = false;
    private static webcamPhoto: any;

    private static get relativeScroll(): RawData['scroll']['relative'] {
        const height = document.body.offsetHeight;
        const width = document.body.offsetWidth;

        let absoluteY = window.pageYOffset;
        let absoluteX = window.pageXOffset;

        let relativeY = 100 * (absoluteY + document.documentElement.clientHeight) / height;
        let relativeX = 100 * (absoluteX + document.documentElement.clientWidth) / width;
        return new ScreenCoordinates(relativeX, relativeY);
    }


    public static async sendCollectionRequest() {
        const objectToSend: RawData = {
            image: ContentScript.takeWebcamPhoto ? ContentScript.webcamPhoto : undefined,
            keyboard: Array.from(ContentScript.keyboard),
            mouse: {
                buttons: Array.from(ContentScript.mouseButtons),
                position: ContentScript.mousePosition
            },
            scroll: {
                absolute: new ScreenCoordinates(window.pageXOffset, window.pageYOffset),
                relative: ContentScript.relativeScroll
            },
            timestamp: Date.now(),
            url: window.location.href,
            width: new ScreenCoordinates(window.innerWidth, window.outerHeight)
        }
        ContentScript.takeWebcamPhoto = false;
        ContentScript.webcamPhoto = undefined;
        chrome.runtime.sendMessage(new Message('data-collected', objectToSend));
    }

    public static registerEvents() {
        window.addEventListener('mousedown', (e: MouseEvent) => {
            ContentScript.mouseButtons.add(e.button);
            ContentScript.sendCollectionRequest();
        });
        window.addEventListener('mouseup', (e: MouseEvent) => {
            ContentScript.mouseButtons.delete(e.button);
            ContentScript.sendCollectionRequest();
        });
        window.addEventListener('mousemove', e => {
            ContentScript.mousePosition.set(e.clientX, e.clientY);
            ContentScript.sendCollectionRequest();
        });
        window.addEventListener('keydown', (e: KeyboardEvent) => {
            ContentScript.keyboard.add(e.key);
            ContentScript.sendCollectionRequest();
        });
        window.addEventListener('keyup', (e: KeyboardEvent) => {
            if (!ContentScript.keyboard.delete(e.key)) {
                // Error fix: released a key that was pressed
                // Example: the key '[' emits as '[' on press and 'è' on release on Chrome
                ContentScript.keyboard.clear();
            }
            ContentScript.sendCollectionRequest();
        });
        window.addEventListener('scroll', (e: UIEvent) => {
            if (e.target == window) {
                this.relativeScroll.set(window.pageXOffset, window.pageYOffset);
                ContentScript.sendCollectionRequest();
            }
        });
        window.addEventListener('resize', (e: UIEvent) => {
            if (e.target == window) {
                ContentScript.sendCollectionRequest();
            }
        });
        chrome.runtime.onMessage.addListener(async (request, sender, sendResponse) => {
            if (request.event == 'snapwebcam') {
                if (navigator.userAgent.search("Firefox") !== -1) {
                    window.postMessage({ type: 'ESPOSITOTHESIS___SNAP_WEBCAM' }, '*');
                    window.addEventListener('message', (event) => {
                        if (event.data.type && event.data.type === "ESPOSITOTHESIS___RETURN_WEBCAM_SNAP") {
                            ContentScript.takeWebcamPhoto = true;
                            ContentScript.webcamPhoto = event.data.snap;
                            ContentScript.sendCollectionRequest();
                        }
                    });
                } else {
                    ContentScript.takeWebcamPhoto = true;
                    ContentScript.webcamPhoto = request.data;
                    ContentScript.sendCollectionRequest();
                }
            }
        });
    }
}
