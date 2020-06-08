import { ScreenCoordinates, Message, RawData, MessageEvents } from "./common-types";

export default class ContentScript {
    private static canSend = true;
    private static isEnabled = true;
    private static hasRegisteredEvents = false;
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

    public static enableWebcam(): void {
        if (navigator.userAgent.search("Firefox") === -1) {
            // Chrome
            if (!document.getElementById("ESPOSITO_THESIS_WEBCAM_IFRAME")) {
                const iframe = document.createElement("iframe");
                iframe.id = "ESPOSITO_THESIS_WEBCAM_IFRAME";
                iframe.src = chrome.extension.getURL("assets/permissions-requester.html");
                iframe.style.display = "none";
                iframe.setAttribute("allow", "camera");
                document.body.appendChild(iframe);
                chrome.runtime.sendMessage(new Message("webcampermission"));
            }
        } else {
            browser.runtime.sendMessage({ event: "firefoxstartwebcam" });
        }
    }

    public static stopWebcam(): void {
        if (navigator.userAgent.search("Firefox") === -1) {
            // Chrome
            const iframe = document.getElementById("ESPOSITO_THESIS_WEBCAM_IFRAME");
            if (iframe) iframe.parentElement.removeChild(iframe);
            chrome.runtime.sendMessage(new Message("stopwebcampermission"));
        } else {
            browser.runtime.sendMessage({ event: "firefoxstopwebcam" });
        }

        ContentScript.isEnabled = false;
    }

    public static sendCollectionRequest(): void {
        if (!ContentScript.isEnabled || !ContentScript.canSend) return;

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
        chrome.storage.local.get((items) => {
            console.warn("NOW", items);
            if (!items.isExtensionActive) {
                ContentScript.isEnabled = false;
                return;
            } else {
                ContentScript.isEnabled = true;
            }
            // if (ContentScript.hasRegisteredEvents) return;

            ContentScript.hasRegisteredEvents = true;
            ContentScript.enableWebcam();
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
            chrome.runtime.onMessage.addListener((request: Message<keyof MessageEvents>) => {
                if (request.event === "snapwebcam") {
                    ContentScript.takeWebcamPhoto = true;
                    ContentScript.webcamPhoto = (request as Message<"snapwebcam">).data;
                    ContentScript.sendCollectionRequest();
                } else if (request.event === "browserfocuschange") {
                    ContentScript.canSend = (request as Message<"browserfocuschange">).data.inFocus;
                }
                //  else if (request.event === "enabledisableextension") {
                // ContentScript.isEnabled = (request as Message<"enabledisableextension">).data.enabled;
                // if (ContentScript.isEnabled) {
                // if (!ContentScript.hasRegisteredEvents) {
                // ContentScript.registerEvents();
                // }
                // ContentScript.enableWebcam();
                // } else {
                // ContentScript.stopWebcam();
                // }
                // }
            });
        });
    }
}
