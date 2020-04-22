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

import * as _ from "lodash";
import * as $ from 'jquery';
import WebcamFacade from "./webcam-facade";
import { response } from "express";

/**
 * The structure of the collected data.
 */
export type CollectedData = {
    ui: string, ///< The user ID
    timestamp: number, ///< The timestamp
    url: string, ///< The visited URL
    mouse: { ///< Various data regarding the mouse
        position: [number, number], ///< The mouse position. p[0] is the X position, p[1] is the Y position.
        buttons: { ///< The mouse buttons
            left: boolean, ///< Is the left button pressed?
            middle: boolean, ///< Is the middle button pressed?
            right: boolean ///< Is the right button pressed?
        }
    },
    scroll: { ///< Various data about the scroll position
        absolute: [number, number] ///< The absolute scroll position. a[0] is the X position, a[1] is the Y position.
        relative: [number, number] ///< The relative scroll position (from the bottom of the screen). r[0] is the X position, r[1] is the Y position.
    },
    width: [number, number], ///< Various data about the browser's window. w[0] is the width, w[1] is the height.
    keyboard: { ///< An array of keys that's currently pressed
        alpha: boolean, ///< Is a alphabetic key pressed?
        numeric: boolean, ///< Is a numeric key pressed?
        symbol: boolean, ///< Is a symbol key pressed?
        function: boolean ///< Is a function key pressed?
    },
    image: string, ///< The webcam snapshot as a data URI.
}

/**
 * The available options for the data collection.
 */
export type CollectionOptions = {
    mainInterval?: number, // defaults to 100 ms
    emotionsInterval?: number, // defaults to 100 ms
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
                    if (!this.pressedKeys.delete(request.keyboard.key)) {
                        // Error fix: released a key that was pressed
                        // Example: the key '[' emits as '[' on press and 'è' on release on Chrome
                        this.pressedKeys.clear();
                    }
                    break;
                case 'webcampermission':
                    WebcamFacade.enableWebcam();
                    break;
            }
        });
        this._areListenersRegistered = true;
    }

    public static getKeyType(key: string) {
        key = key.toString().normalize('NFD').replace(/[\u0300-\u036f]/g, "");
        // The following 'if's will fail if the key's length not equal to 1
        if (/^[a-zA-Z]$/i.test(key)) {
            return 'a';
        }
        else if (/^[0-9]$/.test(key)) {
            return 'n';
        }
        else if (/^[|\\!"£$%&/()=?^'-_.:,;#@+*\[\]]$/.test(key)) {
            return 's';
        }
        else {
            return 'f';
        }
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
    async getURL({ url }: CollectionOptions): Promise<CollectedData['u']> {
        return await new Promise<string>(resolve => {
            chrome.tabs.query({ active: true, lastFocusedWindow: true }, function (tabs) {
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
        let types = new Set<string>([...this.pressedKeys].map(k => Collector.getKeyType(k)));
        return {
            a: types.has('a'),
            f: types.has('f'),
            n: types.has('n'),
            s: types.has('s')
        };
    }

    /**
     * Get the data about the scroll position.
     *
     * @note The relative position is based on the lowest point of the screen.
     */
    async getScrollData(): Promise<CollectedData['s']> {
        return await new Promise<CollectedData['s']>(resolve => {
            chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
                if (tabs === undefined || tabs[0] === undefined || tabs[0].id === undefined) {
                    resolve(null);
                } else {
                    chrome.tabs.sendMessage(tabs[0].id, { event: 'getscrolllocation' }, function (response) {
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
            chrome.tabs.query({ active: true }, function (tabs) {
                if (tabs === undefined || tabs[0] === undefined || tabs[0].id === undefined) {
                    resolve(null);
                } else {
                    chrome.tabs.sendMessage(tabs[0].id, { event: 'getwindowsize' }, function (response) {
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
        if (typeof browser === 'undefined' || navigator.userAgent.search("Firefox") === -1) {
            return WebcamFacade.isEnabled ? await WebcamFacade.snapPhoto() : null;
        }
        return await new Promise<CollectedData['i']>(resolve => {
            browser.tabs.query({ active: true, currentWindow: true })
                .then((tabs) => {
                    if (tabs === undefined || tabs[0] === undefined || tabs[0].id === undefined) {
                        resolve(null);
                    } else {
                        browser.tabs.sendMessage(tabs[0].id, { event: 'snapwebcam' })
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
     * @param photo Wether or not to get the webcam snapshot
     */
    async getData(options: CollectionOptions, photo: boolean): Promise<CollectedData> {
        return {
            ui: this.userId,
            t: Date.now(),
            u: await this.getURL(options),
            m: this.getMouseData(),
            s: await this.getScrollData(),
            w: await this.getWindowData(),
            k: this.getKeyboardData(),
            i: photo ? await Collector.getPhoto() : null,
        };
    }

    /**
     * Send a batch of data to the server.
     * @param data The data to be sent.
     */
    public static sendToServer(data: CollectedData[]): JQuery.jqXHR {
        console.log(data.filter(d=>d.i))
        const URL = 'https://giuseppe-desolda.ddns.net:8080/data/store';
        return $.post(URL, { data: JSON.stringify(data) });
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
        mainInterval: 10,
        emotionsInterval: 100,
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
    let cyclesForEmotion = Math.floor(options.emotionsInterval / options.mainInterval);
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
            numberOfCycles++;
            // If we have to send a snapshot, reset the counter
            let hasToSendSnapshot = (numberOfCycles === cyclesForEmotion);
            if (hasToSendSnapshot) numberOfCycles = 0;
            resultChunk.push(await collector.getData(options, hasToSendSnapshot));
        }, options.mainInterval);
    };

    collectionLoop();
    setInterval(collectionLoop, options.sendInterval);
}
