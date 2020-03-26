import * as _ from "lodash";


export interface CollectedData {
    timestamp: string,
    url: string,
}

export interface CollectionOptions {
    url?: {
        getProtocol?: boolean,
        getDomain?: boolean,
        getPath?: boolean,
        getQuery?: boolean,
        getAnchor?: boolean
    }
}

export class Collector {
    static async getURL(options: CollectionOptions): Promise<string> {
        return await new Promise<string>((resolve, reject) => {
            chrome.tabs.query({active: true, lastFocusedWindow: true}, function (tabs) {
                const {groups} = /^(?<protocol>.*?):\/\/(?<domain>[^/]*?)(?:\/|$)(?<path>[^?]*?)(?:(?:\?|$)(?<query>[^#]*?))?(?:#|$)(?<anchor>.*?)$/.exec(tabs[0].url);

                let url = '';
                options.url.getProtocol && (url += groups.protocol + '://');
                options.url.getDomain && (url += groups.domain + '/');
                options.url.getPath && (url += groups.path);
                options.url.getQuery && (url += '?' + groups.query);
                options.url.getAnchor && (url += '#' + groups.anchor);
                resolve(url);
            });
        });
    }
}


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