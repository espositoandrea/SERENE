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

import './contentscript.scss';
import ContentScript from "./content-utilities";


ContentScript.registerEvents();


// { w: e.target.outerWidth, h: e.target.outerHeight }

function getScroll() {
    const height = document.body.offsetHeight;
    const width = document.body.offsetWidth;

    let absoluteY = window.pageYOffset;
    let absoluteX = window.pageXOffset;

    let relativeY = 100 * (absoluteY + document.documentElement.clientHeight) / height;
    let relativeX = 100 * (absoluteX + document.documentElement.clientWidth) / width;

    return {
        a: [absoluteX, absoluteY],
        r: [relativeX, relativeY]
    };
}

function getWindowSize() {
    return [window.outerWidth, window.outerHeight];
}

// Add listener for messages from the extension process
chrome.runtime.onMessage.addListener(function (request, sender, sendResponse) {
    if (request.event == 'snapwebcam') {
        window.postMessage({ type: 'ESPOSITOTHESIS___SNAP_WEBCAM' }, '*');
        window.addEventListener('message', function (event) {
            if (event.data.type && event.data.type === "ESPOSITOTHESIS___RETURN_WEBCAM_SNAP") {
                sendResponse(event.data.snap)
            }
        });
    }
});

if (navigator.userAgent.search("Firefox") === -1) {
    // Chrome
    let iframe = document.createElement('iframe');
    iframe.src = chrome.extension.getURL("assets/permissions-requester.html");
    iframe.style.display = 'none';
    iframe.setAttribute('allow', 'camera');
    document.body.appendChild(iframe);
    chrome.runtime.sendMessage({ event: 'webcampermission' });
}

window.addEventListener('message', function (event) {
    if (event.source != window) return;

    if (event.data.type && event.data.type === "ESPOSITOTHESIS___SET_USER_ID") {
        chrome.runtime.sendMessage({ event: 'surveycompleted', userId: event.data.userId });
    }
});
