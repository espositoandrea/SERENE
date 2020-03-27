import collect from "../collector";

const showStartingSurvey = async () => {
    new Promise<void>(resolve => {
        chrome.runtime.onInstalled.addListener(() => {
            // TODO: Show survey
            console.log("Survey");
        });
    })
};
const showStartingGuide = async () => {
    new Promise<void>(resolve => {
        chrome.runtime.onInstalled.addListener(() => {
            // TODO: Show guide
            console.log("Guide");
        });
    })
};

showStartingSurvey()
    .then(showStartingGuide)
    .then(() => collect());