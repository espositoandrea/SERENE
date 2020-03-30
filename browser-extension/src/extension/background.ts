import collect from "./collector";


const showStartingSurvey = async () => {
    new Promise<void>(resolve => {
        chrome.runtime.onInstalled.addListener((object) => {
            if (object.reason === 'install') {
                chrome.tabs.create({url: "http://localhost:3000/survey/"}, function (tab) {
                    console.log('Opened survey');
                    resolve()
                });
            }
        });
    })
};

showStartingSurvey()
    .then(() => collect());
