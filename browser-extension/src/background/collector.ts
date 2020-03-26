import * as _ from "lodash";

/**
 * The structure of the collected data.
 */
export interface CollectedData {
    timestamp: string,
    url: string,
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
 * This class collects the required data.
 */
export class Collector {
    /**
     * Get the URL currently visited by the user.
     *
     * @param options The url collection options.
     * @return Promise A promise with the collected data.
     */
    static async getURL({url}: CollectionOptions): Promise<string> {
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

    const timestamp = new Date().toISOString();
    const url = await Collector.getURL(options);

    return {timestamp, url};
}