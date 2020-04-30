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

import WebcamFacade from "./webcam-facade";

WebcamFacade.enableWebcam();


browser.runtime.onMessage.addListener(async (request) => {
    if (request.event == "ESPOSITOTHESIS___SNAP_WEBCAM") {
        return { snap: await WebcamFacade.snapPhoto() };
    } else if (request.event == "ESPOSITOTHESIS___STOP_WEBCAM") {
        WebcamFacade.stopWebcam();
    } else if (request.event == "ESPOSITOTHESIS___ENABLE_WEBCAM") {
        WebcamFacade.enableWebcam();
    }
});
