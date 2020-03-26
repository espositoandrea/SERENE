import './contentscript.scss';

import collect from "../collector";

document.addEventListener('mousemove', function (e) {
    let x = e.pageX;
    let y = e.pageY;
    chrome.runtime.sendMessage({event: 'mousemove', mouse: {position: {x, y}}});
});
document.addEventListener('mousedown', function (e) {
    chrome.runtime.sendMessage({event: 'mousedown', mouse: {button: e.button}});
});
document.addEventListener('mouseup', function (e) {
    chrome.runtime.sendMessage({event: 'mouseup', mouse: {button: e.button}});
});

function getScroll() {
    const height = document.body.offsetHeight;
    const width = document.body.offsetWidth;

    let absoluteY = window.pageYOffset;
    let absoluteX = window.pageXOffset;

    let relativeY = 100 * (absoluteY + document.documentElement.clientHeight) / height;
    let relativeX = 100 * (absoluteX + document.documentElement.clientWidth) / width;

    return {
        absolute: {x: absoluteX, y: absoluteY},
        relative: {x: relativeX, y: relativeY}
    };
}

chrome.runtime.onMessage.addListener(function (request, sender, sendResponse) {
    sendResponse(getScroll());
});