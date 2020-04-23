/*
 * The server component create for Andrea Esposito's Bachelor's Thesis.
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

import { config } from "dotenv";
config();
import * as https from "https";
import * as http from "http";
import * as fs from "fs";

import app from "./app";

const hasHTTPS = Boolean(process.env.HTTPS_CERT_KEY && process.env.HTTPS_CERT);
const server = hasHTTPS ? https.createServer({
    key: fs.readFileSync(process.env.HTTPS_CERT_KEY),
    cert: fs.readFileSync(process.env.HTTPS_CERT)
}, app) : http.createServer(app);

server.listen(process.env.PORT, () => {
    console.log(`Listening (HTTP${hasHTTPS ? "S" : ""}) on port ${process.env.PORT}`);
});
