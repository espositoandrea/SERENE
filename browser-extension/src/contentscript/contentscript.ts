import './contentscript.scss';

import collect from "../collector";

document.addEventListener('mousemove', function (e) {
    let x = e.pageX;
    let y = e.pageY;
    chrome.runtime.sendMessage({event: 'mousemove', mouse: {position: {x, y}}});
});
