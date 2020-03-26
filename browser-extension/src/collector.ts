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
        }
    },
}

/**
 * The available options for the data collection.
 */
export interface CollectionOptions {
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

    private static mousePosition: { x: number, y: number } = {x: 0, y: 0};

    /**
     * The Collector constructor. It registers some messaging events.
     */
    private constructor() {
        chrome.runtime.onMessage.addListener(function (request, sender, sendResponse) {
            if (request.event == "mousemove") {
                Collector.mousePosition = request.mouse.position;
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
        return await new Promise<string>((resolve, reject) => {
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
    getMouseData(): { position: { x: number, y: number } } {
        return {position: Collector.mousePosition};
    }
}


/**
 * A facade function that collects all the required data.
 *
 * @param options Various options for the collection
 * @return Promise A promise with the collected data.
 */
export default async function collect(options?: CollectionOptions): Promise<CollectedData> {
    const defaultCollectionOptions: CollectionOptions = {
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

    const timestamp = new Date().toISOString();
    const url = await collector.getURL(options);
    const mouse = collector.getMouseData();

    return {timestamp, url, mouse};
}