/*
 * The browser extension created for Andrea Esposito's Bachelor's Thesis.
 * Copyright (C) 2020  Andrea Esposito <a.esposito39@studenti.uniba.it>
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

import { Message, MessageEvents } from "./common-types";
import configureCollector from "./collector";

chrome.storage.local.set({ isExtensionActive: true });

chrome.runtime.onInstalled.addListener((object) => {
    if (object.reason === "install") {
        chrome.storage.local.set({ userId: undefined });
        chrome.tabs.create({ url: "https://giuseppe-desolda.ddns.net:8080/survey" }, function (tab) {
            console.log("Opened survey on tab ", tab.id);
        });
    }
});

const getUserId: () => Promise<string> = () => new Promise<string>(resolve => {
    chrome.storage.local.get("userId", function (object) {
        if ("userId" in object) {
            resolve(object.userId);
        } else {
            chrome.runtime.onMessage.addListener(function (request: Message<keyof MessageEvents>) {
                if (request.event === "surveycompleted") {
                    const userId = (request as Message<"surveycompleted">).data.userId;
                    chrome.storage.local.set({ userId });
                    resolve((request as Message<"surveycompleted">).data.userId);
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
        if (typeof browser !== "undefined" && browser.runtime && browser.runtime.getBrowserInfo) {
            browser.runtime.getBrowserInfo()
                .then(info => {
                    if (info.name == "Firefox") {
                        browser.windows.create({
                            url: browser.extension.getURL("assets/firefox-permissions.html"),
                            width: 600,
                            height: 400,
                            type: "normal"
                        })
                            .then(w => localStorage.setItem("popupId", w.id.toString()));
                    }
                });
        }

        configureCollector(userId);
    });
