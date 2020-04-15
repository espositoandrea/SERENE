import * as _ from "lodash";
import * as $ from 'jquery';
import WebcamFacade from "./webcam-facade";
import {response} from "express";

/**
 * The structure of the collected data.
 */
export type CollectedData = {
    ui: string, ///< The user ID
    t: string, ///< The timestamp
    u: string, ///< The visited URL
    m: { ///< Various data regarding the mouse
        p: [number, number], ///< The mouse position. p[0] is the X position, p[1] is the Y position.
        b: { ///< The mouse buttons
            l: boolean, ///< Is the left button pressed?
            m: boolean, ///< Is the middle button pressed?
            r: boolean ///< Is the right button pressed?
        }
    },
    s: { ///< Various data about the scroll position
        a: [number, number] ///< The absolute scroll position. a[0] is the X position, a[1] is the Y position.
        r: [number, number] ///< The relative scroll position (from the bottom of the screen). r[0] is the X position, r[1] is the Y position.
    },
    w: [number, number], ///< Various data about the browser's window. w[0] is the width, w[1] is the height.
    k: string[], ///< An array of keys that's currently pressed
    i: string, ///< The webcam snapshot as a data URI.
}

/**
 * The available options for the data collection.
 */
export type CollectionOptions = {
    mainInterval?: number, // defaults to 100 ms
    sendInterval?: number, // defaults to 5000 ms
    url?: {
        getProtocol?: boolean,
        getDomain?: boolean,
        getPath?: boolean,
        getQuery?: boolean,
        getAnchor?: boolean
    }
}

/**
 * The main collector.
 *
 * This class collects the required data.
 */
export class Collector {
    private mousePosition: CollectedData['m']['p'] = [0, 0];
    private mouseButtons: CollectedData['m']['b'] = {
        l: false,
        m: false,
        r: false
    };
    private pressedKeys: Set<string> = new Set<string>();
    private readonly userId: string;

    private _areListenersRegistered: boolean = false;

    private registerListeners() {
        if (this._areListenersRegistered) return;

        chrome.runtime.onMessage.addListener((request) => {
            let mouseButtonFromInteger = (btn: number) => btn < 3 ? ['l', 'm', 'r'][btn] : 'b' + (btn + 1);

            switch (request.event) {
                case "mousemove":
                    this.mousePosition = request.mouse.position;
                    break;
                case "mousedown":
                    this.mouseButtons[mouseButtonFromInteger(request.mouse.button)] = true;
                    break;
                case "mouseup":
                    this.mouseButtons[mouseButtonFromInteger(request.mouse.button)] = false;
                    break;
                case "keydown":
                    this.pressedKeys.add(request.keyboard.key);
                    break;
                case "keyup":
                    this.pressedKeys.delete(request.keyboard.key);
                    break;
                case 'webcampermission':
                    WebcamFacade.enableWebcam();
                    break;
            }
        });
        this._areListenersRegistered = true;
    }

    /**
     * The Collector constructor. It registers some messaging events.
     */
    public constructor(userId: string) {
        this.registerListeners();
        this.userId = userId;
    }

    /**
     * Get the URL currently visited by the user.
     *
     * @param options The url collection options.
     * @return Promise A promise with the collected data.
     */
    async getURL({url}: CollectionOptions): Promise<CollectedData['u']> {
        return await new Promise<string>(resolve => {
            chrome.tabs.query({active: true, lastFocusedWindow: true}, function (tabs) {
                if (!tabs || !tabs[0] || !tabs[0].url) {
                    resolve(null);
                } else {
                    const regexResult = /^(.*?):\/\/([^/]*?)(?:\/|$)([^?]*?)(?:(?:\?|$)([^#]*?))?(?:#|$)(.*?)$/.exec(tabs[0].url);

                    if (!regexResult) {
                        resolve(null);
                    } else {
                        let outUrl = '';
                        url.getProtocol && (outUrl += regexResult[1] + '://');
                        url.getDomain && (outUrl += regexResult[2] + '/');
                        url.getPath && (outUrl += regexResult[3]);
                        url.getQuery && regexResult[4] && (outUrl += '?' + regexResult[4]);
                        url.getAnchor && regexResult[5] && (outUrl += '#' + regexResult[5]);
                        resolve(outUrl);
                    }
                }
            });
        });
    }

    /**
     * Get all the information about the mouse.
     *
     * @return Object The mouse data.
     */
    getMouseData(): CollectedData['m'] {
        return {
            p: this.mousePosition,
            b: this.mouseButtons,
        };
    }

    /**
     * Get all the information about the keyboard.
     *
     * @return Object The keyboard data.
     */
    getKeyboardData(): CollectedData['k'] {
        return Array.from(this.pressedKeys);
    }

    /**
     * Get the data about the scroll position.
     *
     * @note The relative position is based on the lowest point of the screen.
     */
    async getScrollData(): Promise<CollectedData['s']> {
        return await new Promise<CollectedData['s']>(resolve => {
            chrome.tabs.query({active: true, currentWindow: true}, function (tabs) {
                if (tabs === undefined || tabs[0] === undefined || tabs[0].id === undefined) {
                    resolve(null);
                } else {
                    chrome.tabs.sendMessage(tabs[0].id, {event: 'getscrolllocation'}, function (response) {
                        if (chrome.runtime.lastError) {
                            // The target page has disabled the execution of
                            // content scripts
                            resolve(null);
                        } else {
                            resolve(response);
                        }
                    });
                }
            });
        });
    }

    /**
     * Get the data about the scroll position.
     *
     * @note The relative position is based on the lowest point of the screen.
     */
    async getWindowData(): Promise<CollectedData['w']> {
        return await new Promise<CollectedData['w']>(resolve => {
            chrome.tabs.query({active: true}, function (tabs) {
                if (tabs === undefined || tabs[0] === undefined || tabs[0].id === undefined) {
                    resolve(null);
                } else {
                    chrome.tabs.sendMessage(tabs[0].id, {event: 'getwindowsize'}, function (response) {
                        if (chrome.runtime.lastError) {
                            // The target page has disabled the execution of
                            // content scripts
                            resolve(null);
                        } else {
                            resolve(response);
                        }
                    });
                }
            });
        });
    }

    static async getPhoto(): Promise<CollectedData['i']> {
        if (navigator.userAgent.search("Firefox") === -1) {
            return WebcamFacade.isEnabled ? await WebcamFacade.snapPhoto() : null;
        }
        return await new Promise<CollectedData['i']>(resolve => {
            browser.tabs.query({active: true, currentWindow: true})
                .then((tabs) => {
                    if (tabs === undefined || tabs[0] === undefined || tabs[0].id === undefined) {
                        resolve(null);
                    } else {
                        browser.tabs.sendMessage(tabs[0].id, {event: 'snapwebcam'})
                            .then(async response => {
                                if (browser.runtime.lastError) {
                                    resolve(null);
                                } else {
                                    resolve(await response);
                                }
                            });
                    }
                });
        });
    }

    /**
     * Get all the required data.
     * @param options Various collection options
     */
    async getData(options: CollectionOptions): Promise<CollectedData> {
        return {
            ui: this.userId,
            t: new Date().toISOString(),
            u: await this.getURL(options),
            m: this.getMouseData(),
            s: await this.getScrollData(),
            w: await this.getWindowData(),
            k: this.getKeyboardData(),
            i: await Collector.getPhoto()
        };
    }

    /**
     * Send a batch of data to the server.
     * @param data The data to be sent.
     */
    public static sendToServer(data: CollectedData[]): JQuery.jqXHR {
        const URL = 'http://giuseppe-desolda.ddns.net:8080/data/store';
        return $.post(URL, {data: JSON.stringify(data)});
    }
}


/**
 * A facade function that collects all the required data.
 *
 * @param userId The user ID
 * @param options Various options for the collection
 * @return Promise A promise with the collected data.
 */
export default function collect(userId: string, options?: CollectionOptions): void {
    if (!userId) return;

    const defaultCollectionOptions: CollectionOptions = {
        mainInterval: 100,
        sendInterval: 5000,
        url: {
            getProtocol: true,
            getDomain: true,
            getPath: false,
            getQuery: false,
            getAnchor: false
        }
    };
    options = _.merge(defaultCollectionOptions, options || {});

    const collector = new Collector(userId);

    // To simplify the management of the intervals, the interval of the
    // analysis that include the emotions (EA - Emotion Analysis) is used to
    // get the number of analysis without emotions between one EA and another.
    let numberOfCycles = 0;
    let resultChunk: CollectedData[] = [];

    let collectorInterval: any = undefined;

    let collectionLoop = () => {
        if (collectorInterval !== undefined) {
            clearInterval(collectorInterval);
            Collector.sendToServer(resultChunk)
                .done(() => resultChunk = [])
                .fail((data, status, error) => console.error(error));
        }

        collectorInterval = setInterval(async function () {
            resultChunk.push(await collector.getData(options));
            numberOfCycles++;
        }, options.mainInterval);
    };

    collectionLoop();
    setInterval(collectionLoop, options.sendInterval);
}
