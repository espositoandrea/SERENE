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

import * as express from "express";
import * as fs from "fs";
import * as bodyParser from "body-parser";
import { MongoClient } from "mongodb";
import * as cors from "cors";

import router from "./routes";

const app: express.Application = express();
const requestSizeLimit = "50mb";

if (!fs.existsSync("temp")) {
    console.log("Creating temp/ directory");
    fs.mkdirSync("temp");
}

app.use(bodyParser.json({ limit: requestSizeLimit }));
app.use(bodyParser.urlencoded({ limit: requestSizeLimit, extended: false }));
app.use(bodyParser.raw({ limit: requestSizeLimit }));
app.use(cors());

app.use("/assets", express.static("assets"));
app.use("/downloads", express.static("downloads"));

MongoClient.connect(process.env.DB_HOST, { useUnifiedTopology: true }, (err, client) => {
    if (err) return console.log(err);
    const db = client.db(process.env.DB_NAME);

    app.use(router(db));
});

export default app;
