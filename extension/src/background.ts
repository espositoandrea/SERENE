import collect from "./collector";


chrome.runtime.onInstalled.addListener((object) => {
    if (object.reason === 'install') {
        chrome.storage.local.set({userId: undefined});
        chrome.tabs.create({url: "http://giuseppe-desolda.ddns.net:8080/survey"}, function (tab) {
            console.log('Opened survey');
        });
    }
});

const getUserId = () => new Promise<string>(resolve => {
    chrome.storage.local.get('userId', function (object) {
        if ('userId' in object) {
            resolve(object.userId)
        } else {
            chrome.runtime.onMessage.addListener(function (request, sender, response) {
                if (request.event == 'surveycompleted') {
                    const userId = request.userId;
                    chrome.storage.local.set({userId});
                    resolve(request.userId);
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
        if (browser && browser.runtime && browser.runtime.getBrowserInfo) {
            browser.runtime.getBrowserInfo()
                .then(info => {
                    if (info.name == "Firefox") {
                        browser.windows.create({
                            url: browser.extension.getURL('assets/firefox-permissions.html'),
                            width: 600,
                            height: 400,
                            type: "popup"
                        });
                    }
                });
        }

        collect(userId);
    });
