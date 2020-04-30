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

import "./contentscript.scss";
import ContentScript from "./content-utilities";
import { Message, MessageEvents } from "./common-types";

ContentScript.registerEvents();

window.addEventListener("message", function (event) {
    if (event.source != window) return;

    if (event.data.type && event.data.type === "ESPOSITOTHESIS___SET_USER_ID") {
        chrome.runtime.sendMessage(new Message("surveycompleted", { userId: event.data.userId }));
    }
});

chrome.runtime.onMessage.addListener((request: Message<keyof MessageEvents>) => {
    if (request.event === "enabledisableextension") {
        const isEnabled = (request as Message<"enabledisableextension">).data.enabled;
        if (isEnabled) {
            ContentScript.enableWebcam();
            ContentScript.registerEvents();
        } else {
            ContentScript.stopWebcam();
        }
    }
});
