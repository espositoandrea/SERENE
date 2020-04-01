import collect from "./collector";
import { resolve } from "dns";


chrome.runtime.onInstalled.addListener((object) => {
    if (object.reason === 'install') {
        chrome.tabs.create({ url: "http://localhost:3000/survey/" }, function (tab) {
            console.log('Opened survey');
        });
    }
});

const getUserId = () => new Promise<string>(resolve => {
    chrome.storage.local.get('userId', function (object) {
        if ('userId' in object) {
            resolve(object.userId)
        }
        else {
            chrome.runtime.onMessageExternal.addListener(function (request, sender, response) {
                if (request.event == 'surveycompleted') {
                    const userId = request.userId;
                    chrome.storage.local.set({ userId });
                    resolve(object.userId);
                }
            });
        }
    });
});

getUserId()
    .then((userId) => {
        if (!userId) {
            alert("Impossibile utilizzare l'estensione se non si è compilato il questionario.");
            return;
        }
        collect(userId)
    });
