import * as _ from "lodash";
import tabId = chrome.devtools.inspectedWindow.tabId;
import EmotionAnalysis from "./emotion-analysis/emotion-analysis";

/**
 * The structure of the collected data.
 */
export interface CollectedData {
    timestamp: string,
    url: string,
    mouse: {
        position: {
            x: number,
            y: number
        },
        buttons: {
            leftPressed: boolean,
            middlePressed: boolean,
            rightPressed: boolean
        }
    },
    scroll: {
        absolute: { x: number, y: number },
        relative: { x: number, y: number }
    },
    keyboard: string[],
    emotions: any
}

/**
 * The available options for the data collection.
 */
export interface CollectionOptions {
    mainInterval?: number, // defaults to 100 ms
    emotionsInterval?: number, // defaults to 1000 ms
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
 * This singleton class collects the required data.
 */
export class Collector {
    private static instance: Collector;

    private mousePosition: CollectedData['mouse']['position'] = {x: 0, y: 0};
    private mouseButtons: CollectedData['mouse']['buttons'] = {
        leftPressed: false,
        middlePressed: false,
        rightPressed: false
    };
    private pressedKeys: Set<string> = new Set<string>();

    /**
     * The Collector constructor. It registers some messaging events.
     */
    private constructor() {
        chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
            let mouseButtonFromInteger = (btn: number) => btn < 3 ? ['left', 'middle', 'right'][btn] : 'button' + (btn + 1);

            switch (request.event) {
                case "mousemove":
                    this.mousePosition = request.mouse.position;
                    break;
                case "mousedown":
                    this.mouseButtons[mouseButtonFromInteger(request.mouse.button) + 'Pressed'] = true;
                    break;
                case "mouseup":
                    this.mouseButtons[mouseButtonFromInteger(request.mouse.button) + 'Pressed'] = false;
                    break;
                case "keydown":
                    this.pressedKeys.add(request.keyboard.key);
                    break;
                case "keyup":
                    this.pressedKeys.delete(request.keyboard.key);
                    break;
            }
        });
    }

    /**
     * Get the instance of the Collector.
     */
    public static getInstance(): Collector {
        if (!Collector.instance) {
            Collector.instance = new Collector();
        }
        return Collector.instance;
    }

    /**
     * Get the URL currently visited by the user.
     *
     * @param options The url collection options.
     * @return Promise A promise with the collected data.
     */
    async getURL({url}: CollectionOptions): Promise<string> {
        return await new Promise<string>(resolve => {
            chrome.tabs.query({active: true, lastFocusedWindow: true}, function (tabs) {
                if (tabs === undefined || tabs[0] === undefined || tabs[0].url === undefined) {
                    resolve(null);
                } else {
                    const {groups} = /^(?<protocol>.*?):\/\/(?<domain>[^/]*?)(?:\/|$)(?<path>[^?]*?)(?:(?:\?|$)(?<query>[^#]*?))?(?:#|$)(?<anchor>.*?)$/.exec(tabs[0].url);

                    let outUrl = '';
                    url.getProtocol && (outUrl += groups.protocol + '://');
                    url.getDomain && (outUrl += groups.domain + '/');
                    url.getPath && (outUrl += groups.path);
                    url.getQuery && (outUrl += '?' + groups.query);
                    url.getAnchor && (outUrl += '#' + groups.anchor);
                    resolve(outUrl);
                }
            });
        });
    }

    /**
     * Get all the information about the mouse.
     *
     * @return Object The mouse data.
     */
    getMouseData(): CollectedData['mouse'] {
        return {
            position: this.mousePosition,
            buttons: this.mouseButtons,
        };
    }

    /**
     * Get all the information about the keyboard.
     *
     * @return Object The keyboard data.
     */
    getKeyboardData(): CollectedData['keyboard'] {
        return Array.from(this.pressedKeys);
    }

    /**
     * Get the data about the scroll position.
     *
     * @note The relative position is based on the lowest point of the screen.
     */
    async getScrollData(): Promise<CollectedData['scroll']> {
        return await new Promise<CollectedData['scroll']>(resolve => {
            chrome.tabs.query({active: true, currentWindow: true}, function (tabs) {
                if (tabs === undefined || tabs[0] === undefined || tabs[0].id === undefined) {
                    resolve(null);
                } else {
                    chrome.tabs.sendMessage(tabs[0].id, {event: 'getscrolllocation'}, function (response) {
                        resolve(response);
                    });
                }
            });
        });
    }

    async getEmotions(): Promise<CollectedData['emotions']> {
        let emotions;
        try {
            emotions = await EmotionAnalysis.getInstance().analyzeWebcamPhoto();
        } catch (e) {
            emotions = null;
            console.error(e.message);
        }
        return emotions;
    }

    /**
     * Get all the required data.
     * @param options Various collection options
     */
    async getData(options: CollectionOptions): Promise<CollectedData> {
        const data = await this.getDataNoEmotions(options);
        data.emotions = await this.getEmotions();
        return data;
    }

    /**
     * Get all the required data except for the emotions.
     * @param options Various collection options
     */
    async getDataNoEmotions(options: CollectionOptions): Promise<CollectedData> {
        return {
            timestamp: new Date().toISOString(),
            url: await this.getURL(options),
            mouse: this.getMouseData(),
            scroll: await this.getScrollData(),
            keyboard: this.getKeyboardData(),
            emotions: null
        };
    }
}


/**
 * A facade function that collects all the required data.
 *
 * @param options Various options for the collection
 * @return Promise A promise with the collected data.
 */
export default function collect(options?: CollectionOptions): void {
    const defaultCollectionOptions: CollectionOptions = {
        mainInterval: 100,
        emotionsInterval: 1000,
        sendInterval: 5000,
        url: {
            getProtocol: true,
            getDomain: true,
            getPath: false,
            getQuery: false,
            getAnchor: false
        }
    };
    options = _.merge(defaultCollectionOptions, options ?? {});

    const collector = Collector.getInstance();

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
            // TODO: Send resultChunk to server
            console.log(resultChunk);
            resultChunk = [];
        }

        collectorInterval = setInterval(async function () {
            if (numberOfCycles % cyclesForEmotion == 0) {
                // TODO: Insert emotion collection
                // collector.getEmotions()
                //     .then((val) => resultChunk[resultChunk.length - 1].emotions = val)
                resultChunk.push(await collector.getDataNoEmotions(options));
            } else {
                resultChunk.push(await collector.getDataNoEmotions(options));
            }
            numberOfCycles++;
        }, options.mainInterval);
    };

    collectionLoop();
    setInterval(collectionLoop, options.sendInterval);
}