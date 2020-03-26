import collect from "../collector";

const updateTabsContent = async () => {
    new Promise<void>(resolve => {
        chrome.runtime.onInstalled.addListener(() => {
            // chrome.tabs.query({}, (tabs) => {
            //     chrome.tabs.reload(tabs[0].id, null, () => resolve());
            // });
        });
    })
};

updateTabsContent()
    .then(() => collect());
