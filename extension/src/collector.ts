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
import * as $ from "jquery";
import WebcamFacade from "./webcam-facade";
import { ScreenCoordinates, RawData, KeyboardKey, Message, MessageEvents } from "./common-types";

/**
 * The structure of the collected data.
 */
export type CollectedData = {
    userId: string; ///< The user ID
    timestamp: number; ///< The timestamp
    url: string; ///< The visited URL
    mouse: { ///< Various data regarding the mouse
        position: ScreenCoordinates; ///< The mouse position.
        buttons: { ///< The mouse buttons
            left: boolean; ///< Is the left button pressed?
            middle: boolean; ///< Is the middle button pressed?
            right: boolean; ///< Is the right button pressed?
            [key: string]: boolean; ///< Are other buttons pressed?
        };
    };
    scroll: { ///< Various data about the scroll position
        absolute: ScreenCoordinates; ///< The absolute scroll position.
        relative: ScreenCoordinates; ///< The relative scroll position (from the bottom of the screen).
    };
    window: ScreenCoordinates; ///< Various data about the browser's window. w[0] is the width, w[1] is the height.
    keyboard: { ///< An array of keys that's currently pressed
        alpha: boolean; ///< Is a alphabetic key pressed?
        numeric: boolean; ///< Is a numeric key pressed?
        symbol: boolean; ///< Is a symbol key pressed?
        function: boolean; ///< Is a function key pressed?
    };
    image: string; ///< The webcam snapshot as a data URI.
}

/**
 * The available options for the data collection.
 */
export type CollectionOptions = {
    focusCheckInterval?: number; // defaults to 50 ms
    emotionsInterval?: number; // defaults to 100 ms
    sendInterval?: number; // defaults to 5000 ms
    url?: {
        getProtocol?: boolean;
        getDomain?: boolean;
        getPath?: boolean;
        getQuery?: boolean;
        getAnchor?: boolean;
    };
}

/**
 * The main collector.
 *
 * This class collects the required data.
 */
export class Collector {
    private readonly userId: string;

    /**
     * The Collector constructor. It registers some messaging events.
     */
    public constructor(userId: string) {
        this.userId = userId;
    }

    private static getUrl(url, urlOptions: CollectionOptions["url"]): CollectedData["url"] | null {
        const regexResult = /^(.*?):\/\/([^/]*?)(?:\/|$)([^?]*?)(?:(?:\?|$)([^#]*?))?(?:#|$)(.*?)$/.exec(url);

        if (!regexResult) {
            return null;
        } else {
            let outUrl = "";
            urlOptions.getProtocol && (outUrl += regexResult[1] + "://");
            urlOptions.getDomain && (outUrl += regexResult[2] + "/");
            urlOptions.getPath && (outUrl += regexResult[3]);
            urlOptions.getQuery && regexResult[4] && (outUrl += "?" + regexResult[4]);
            urlOptions.getAnchor && regexResult[5] && (outUrl += "#" + regexResult[5]);
            return outUrl;
        }
    }

    private static getKeyboardData(pressedKeys: Set<string>): CollectedData["keyboard"] {
        const types = new Set<KeyboardKey.Types>([...pressedKeys].map(k => KeyboardKey.getType(k)));
        return {
            alpha: types.has(KeyboardKey.Types.ALPHABETIC),
            function: types.has(KeyboardKey.Types.FUNCTION),
            numeric: types.has(KeyboardKey.Types.NUMERIC),
            symbol: types.has(KeyboardKey.Types.SYMBOLIC)
        };
    }

    private static getMouseButtons(buttons: Set<number>): CollectedData["mouse"]["buttons"] {
        const obj: CollectedData["mouse"]["buttons"] = {
            left: buttons.has(0),
            middle: buttons.has(1),
            right: buttons.has(2)
        };

        buttons.forEach(button => {
            if (button > 2) {
                obj["button" + (button + 1)] = true;
            }
        });

        return obj;
    }

    public process(data: RawData, options: CollectionOptions): CollectedData {
        return {
            image: data.image,
            mouse: {
                buttons: Collector.getMouseButtons(new Set<number>(data.mouse.buttons)),
                position: data.mouse.position
            },
            keyboard: Collector.getKeyboardData(new Set<string>(data.keyboard)),
            scroll: data.scroll,
            timestamp: data.timestamp,
            url: Collector.getUrl(data.url, options.url ?? {}),
            userId: this.userId,
            window: data.window
        };
    }
}

/**
 * Send a batch of data to the server.
 * @param data The data to be sent.
 */
function sendToServer(data: CollectedData[]): JQuery.jqXHR {
    if (data.length == 0) return;

    const URL = "https://giuseppe-desolda.ddns.net:8080/data/store";
    return $.post(URL, { data: JSON.stringify(data) });
}

function collect(userId: string, collectedData: RawData, options: CollectionOptions): CollectedData {
    const collector = new Collector(userId);
    const finalData: CollectedData = collector.process(collectedData, options);
    return finalData;
}

function askForWebcamSnapshot(): void {
    if (typeof browser !== "undefined" && browser.runtime && browser.runtime.getBrowserInfo && localStorage.getItem("popupId")) {
        browser.tabs.query({ windowId: parseInt(localStorage.getItem("popupId")) })
            .then(tabs => {
                if (tabs !== undefined && tabs[0] !== undefined && tabs[0].id !== undefined) {
                    browser.tabs.sendMessage(tabs[0].id, { event: "ESPOSITOTHESIS___SNAP_WEBCAM" })
                        .then(response => {
                            browser.tabs.query({ active: true, currentWindow: true })
                                .then(tabs => {
                                    if (tabs !== undefined && tabs[0] !== undefined && tabs[0].id !== undefined) {
                                        browser.tabs.sendMessage(tabs[0].id, { event: "snapwebcam", data: response.snap });
                                    }
                                });
                        });
                }
            });
    }
    else {
        chrome.tabs.query({ active: true, currentWindow: true }, async (tabs) => {
            if (tabs !== undefined && tabs[0] !== undefined && tabs[0].id !== undefined) {
                const photo = (navigator.userAgent.search("Firefox") !== -1) ? undefined : await WebcamFacade.snapPhoto();
                chrome.tabs.sendMessage(tabs[0].id, { event: "snapwebcam", data: photo });
            }
        });
    }
}


let previouslyFocused = true;
function checkBrowserFocus(): void {
    chrome.windows.getCurrent(function (browser) {
        if (browser.focused != previouslyFocused) {
            previouslyFocused = browser.focused;

            chrome.tabs.query({}, async (tabs) => {
                if (tabs !== undefined && tabs[0] !== undefined && tabs[0].id !== undefined) {
                    tabs.forEach(tab => {
                        chrome.tabs.sendMessage(tab.id, new Message("browserfocuschange", { inFocus: previouslyFocused }));
                    });
                }
            });
        }
    });
}

let opened = false;
function setUpSwitchFirefoxWebcamListener(): void {
    if (typeof browser !== "undefined" && browser.runtime && browser.runtime.onMessage && localStorage.getItem("popupId")) {
        browser.runtime.onMessage.addListener((request) => {
            if (request.event == "firefoxstopwebcam") {
                browser.windows.remove(parseInt(localStorage.getItem("popupId")));
                opened = false;
            } else if (request.event == "firefoxstartwebcam" && !opened) {
                opened = true;
                browser.windows.create({
                    url: browser.extension.getURL("assets/firefox-permissions.html"),
                    width: 600,
                    height: 400,
                    type: "normal"
                })
                    .then(w => localStorage.setItem("popupId", w.id.toString()));
            }
        });
    }
}

/**
 * A facade function that collects all the required data.
 *
 * @param userId The user ID
 * @param options Various options for the collection
 * @return Promise A promise with the collected data.
 */
export default function configureCollector(userId: string, options?: CollectionOptions): void {
    if (!userId) return;

    const defaultCollectionOptions: CollectionOptions = {
        focusCheckInterval: 50,
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

    setUpSwitchFirefoxWebcamListener();

    checkBrowserFocus();
    setInterval(checkBrowserFocus, options.focusCheckInterval);

    askForWebcamSnapshot();
    setInterval(askForWebcamSnapshot, options.emotionsInterval);

    let data: CollectedData[] = new Array<CollectedData>();

    setInterval(() => {
        // Send to server and clear collected data
        sendToServer(data).fail((data, status, error) => console.error(error));
        data = new Array<CollectedData>();
    }, options.sendInterval);

    chrome.runtime.onMessage.addListener(function (request: Message<keyof MessageEvents>) {
        if (request.event === "data-collected") {
            data.push(collect(userId, (request as Message<"data-collected">).data, options));
        } else if (request.event === "webcampermission") {
            WebcamFacade.enableWebcam();
        } else if (request.event === "stopwebcampermission") {
            WebcamFacade.stopWebcam();
        }
    });
}
