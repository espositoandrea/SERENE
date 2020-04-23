import { ScreenCoordinates, Message, RawData } from "./common-types";

export default class ContentScript {
    private static readonly keyboard: Set<string> = new Set<string>();
    private static readonly mousePosition: RawData["mouse"]["position"] = new ScreenCoordinates();
    private static readonly mouseButtons: Set<number> = new Set<number>();
    private static takeWebcamPhoto = false;
    private static webcamPhoto: string;

    private static get relativeScroll(): RawData["scroll"]["relative"] {
        const height = document.body.offsetHeight;
        const width = document.body.offsetWidth;

        const absoluteY = window.pageYOffset;
        const absoluteX = window.pageXOffset;

        const relativeY = 100 * (absoluteY + document.documentElement.clientHeight) / height;
        const relativeX = 100 * (absoluteX + document.documentElement.clientWidth) / width;
        return new ScreenCoordinates(relativeX, relativeY);
    }


    public static sendCollectionRequest(): void {
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
            window: new ScreenCoordinates(window.innerWidth, window.outerHeight)
        };
        ContentScript.takeWebcamPhoto = false;
        ContentScript.webcamPhoto = undefined;
        chrome.runtime.sendMessage(new Message("data-collected", objectToSend));
    }

    public static registerEvents(): void {
        window.addEventListener("mousedown", (e: MouseEvent) => {
            ContentScript.mouseButtons.add(e.button);
            ContentScript.sendCollectionRequest();
        });
        window.addEventListener("mouseup", (e: MouseEvent) => {
            ContentScript.mouseButtons.delete(e.button);
            ContentScript.sendCollectionRequest();
        });
        window.addEventListener("mousemove", e => {
            ContentScript.mousePosition.set(e.clientX, e.clientY);
            ContentScript.sendCollectionRequest();
        });
        window.addEventListener("keydown", (e: KeyboardEvent) => {
            ContentScript.keyboard.add(e.key);
            ContentScript.sendCollectionRequest();
        });
        window.addEventListener("keyup", (e: KeyboardEvent) => {
            if (!ContentScript.keyboard.delete(e.key)) {
                // Error fix: released a key that was pressed
                // Example: the key '[' emits as '[' on press and 'è' on release on Chrome
                ContentScript.keyboard.clear();
            }
            ContentScript.sendCollectionRequest();
        });
        window.addEventListener("scroll", (e: UIEvent) => {
            if (e.target == window) {
                this.relativeScroll.set(window.pageXOffset, window.pageYOffset);
                ContentScript.sendCollectionRequest();
            }
        });
        window.addEventListener("resize", (e: UIEvent) => {
            if (e.target == window) {
                ContentScript.sendCollectionRequest();
            }
        });
        chrome.runtime.onMessage.addListener((request) => {
            if (request.event == "snapwebcam") {
                ContentScript.takeWebcamPhoto = true;
                ContentScript.webcamPhoto = request.data;
                ContentScript.sendCollectionRequest();
            }
        });
    }
}
