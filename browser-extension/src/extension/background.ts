import collect from "./collector";


const showStartingSurvey = async () => {
    new Promise<void>(resolve => {
        chrome.runtime.onInstalled.addListener(() => {
            // TODO: Show survey
            console.log("Survey");
            resolve()
        });
    })
};
const showStartingGuide = async () => {
    new Promise<void>(resolve => {
        chrome.runtime.onInstalled.addListener(() => {
            // TODO: Show guide
            console.log("Guide");
            resolve()
        });
    })
};

showStartingSurvey()
    .then(showStartingGuide)
    .then(() => collect());
