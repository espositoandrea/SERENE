import * as _ from "lodash";

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

    private static mousePosition: CollectedData['mouse']['position'] = {x: 0, y: 0};
    private static mouseButtons: CollectedData['mouse']['buttons'] = {
        leftPressed: false,
        middlePressed: false,
        rightPressed: false
    };
    private static scrollLocation = {
        absolute: {x: 0, y: 0},
        relative: {x: 0, y: 0},
    }

    /**
     * The Collector constructor. It registers some messaging events.
     */
    private constructor() {
        chrome.runtime.onMessage.addListener(function (request, sender, sendResponse) {
            let mouseButtonFromInteger = (btn: number) => ['left', 'middle', 'right'][request.mouse.button];

            if (request.event == "mousemove") {
                Collector.mousePosition = request.mouse.position;
            } else if (request.event == "mousedown") {
                Collector.mouseButtons[mouseButtonFromInteger(request.mouse.button) + 'Pressed'] = true;
            } else if (request.event == "mouseup") {
                Collector.mouseButtons[mouseButtonFromInteger(request.mouse.button) + 'Pressed'] = false;
            } else if (request.event == "scroll") {
                console.log(request.mouse);
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
                const {groups} = /^(?<protocol>.*?):\/\/(?<domain>[^/]*?)(?:\/|$)(?<path>[^?]*?)(?:(?:\?|$)(?<query>[^#]*?))?(?:#|$)(?<anchor>.*?)$/.exec(tabs[0].url);

                let outUrl = '';
                url.getProtocol && (outUrl += groups.protocol + '://');
                url.getDomain && (outUrl += groups.domain + '/');
                url.getPath && (outUrl += groups.path);
                url.getQuery && (outUrl += '?' + groups.query);
                url.getAnchor && (outUrl += '#' + groups.anchor);
                resolve(outUrl);
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
            position: Collector.mousePosition,
            buttons: Collector.mouseButtons,
        };
    }

    /**
     * Get the data about the scroll position.
     *
     * @note The relative position is based on the lowest point of the screen.
     */
    async getScrollData(): Promise<CollectedData['scroll']> {
        return await new Promise<CollectedData['scroll']>(resolve => {
            chrome.tabs.query({active: true, currentWindow: true}, function (tabs) {
                chrome.tabs.sendMessage(tabs[0].id, {event: 'getscrolllocation'}, function (response) {
                    resolve(response);
                });
            });
        });
    }

    /**
     * Get all the required data.
     * @param options Various collection options
     */
    async getData(options: CollectionOptions): Promise<CollectedData> {
        const data = await this.getDataNoEmotions(options);
        return {...data};
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
                resultChunk.push(await collector.getData(options));
            } else {
                resultChunk.push(await collector.getDataNoEmotions(options));
            }
            numberOfCycles++;
        }, options.mainInterval);
    };

    collectionLoop();
    setInterval(collectionLoop, options.sendInterval);
}