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

import { Router } from "express";
import DataProcessor from "./data-processor";
import * as path from "path";
import { Db } from "mongodb";
import apiRouter from "./api-routes";

export default function router(db: Db): Router {
    const router = Router();

    router.get("/", (req, res) => res.sendFile(path.resolve("./index.html")));

    router.get("/survey", (req, res) => res.sendFile(path.resolve("./survey.html")));

    router.post("/data/store", async (request, response) => {
        const data = JSON.parse(request.body.data);
        // Data received: notify the sender
        response.send({ done: true, errors: null });

        DataProcessor.process(data)
            .then((data) => {
                db.collection("interactions").insertMany(data, (err, result) => {
                    if (err) {
                        // TODO: There was an error in writing to the DB: handle this error
                        return console.log(err);
                    }

                    console.log("saved to database: inserted " + result.insertedCount + " documents");
                });
            });
    });

    router.post("/survey/store", (request, response) => {
        const userData = {
            age: parseInt(request.body.age),
            gender: request.body.gender,
            internet: parseInt(request.body.internet)
        };

        db.collection("users").insertOne(userData, (err, result) => {
            if (err) {
                // TODO: There was an error in writing to the DB: handle this error
                response.json({ done: false, errors: err });
                return console.log(err);
            }

            response.json({ done: true, errors: [], userId: result.insertedId });
        });
    });

    router.use("/api", apiRouter(db));

    return router;
}
