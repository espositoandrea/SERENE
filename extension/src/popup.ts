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

import { Message } from "./common-types";

chrome.storage.local.get(function (items) {
    const activeAtStart = items.isExtensionActive;
    const extensionSwitch = document.getElementById("extension-switch") as HTMLInputElement;
    const currentStateSpan: HTMLSpanElement = document.getElementById("extension-state");
    currentStateSpan.innerHTML = activeAtStart ? "attiva" : "disattiva";
    extensionSwitch.checked = activeAtStart;

    extensionSwitch.addEventListener("click", function () {
        const active = this.checked;
        chrome.storage.local.set({ isExtensionActive: active });

        chrome.tabs.query({}, async (tabs) => {
            if (tabs !== undefined && tabs[0] !== undefined && tabs[0].id !== undefined) {
                tabs.forEach(tab => {
                    chrome.tabs.sendMessage(tab.id, new Message("enabledisableextension", { enabled: active }));
                });
            }
        });

        currentStateSpan.innerHTML = active ? "attiva" : "disattiva";
    });
});

