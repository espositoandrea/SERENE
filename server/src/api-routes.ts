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
import { Db, ObjectID } from "mongodb";

const limit = 1;

export default function router(db: Db): Router {
    const apiRouter = Router();

    apiRouter.get("/users", function (request, response) {
        db.collection("users")
            .find()
            .toArray()
            .then(arr => response.json(arr));
    });

    apiRouter.get("/users/:skip-:limit", function (request, response) {
        db.collection("users")
            .find()
            .skip(parseInt(request.params.skip) || 0)
            .limit(parseInt(request.params.limit) || 0)
            .toArray()
            .then(arr => response.json(arr));
    });

    apiRouter.get("/interactions", function (request, response) {
        db.collection("interactions")
            .find()
            .toArray()
            .then(arr => response.json(arr));
    });

    apiRouter.get("/interactions/count", function (request, response) {
        db.collection("interactions")
            .countDocuments()
            .then(arr => response.json(arr));
    });

    apiRouter.get("/interactions/:skip-:limit", function (request, response) {
        db.collection("interactions")
            .find()
            .skip(parseInt(request.params.skip) || 0)
            .limit(parseInt(request.params.limit) || 0)
            .toArray()
            .then(arr => response.json(arr));
    });

    apiRouter.get("/interactions/filtered", function (request, response) {
        db.collection("interactions")
            .find({
                $or: [
                    { e: { $exists: false } },
                    { "e.e": { $gte: limit } },
                    { "e.j": { $gte: limit } },
                    { "e.f": { $gte: limit } },
                    { "e.d": { $gte: limit } },
                    { "e.s": { $gte: limit } },
                    { "e.a": { $gte: limit } },
                    { "e.su": { $gte: limit } },
                    { "e.c": { $gte: limit } },
                    { "e.v": { $gte: limit } },
                    { "e.e": { $gte: limit } },
                ]
            })
            .toArray()
            .then(arr => response.json(arr));
    });

    apiRouter.get("/interactions/filtered/count", function (request, response) {
        db.collection("interactions")
            .countDocuments({
                $or: [
                    { e: { $exists: false } },
                    { "e.e": { $gte: limit } },
                    { "e.j": { $gte: limit } },
                    { "e.f": { $gte: limit } },
                    { "e.d": { $gte: limit } },
                    { "e.s": { $gte: limit } },
                    { "e.a": { $gte: limit } },
                    { "e.su": { $gte: limit } },
                    { "e.c": { $gte: limit } },
                    { "e.v": { $gte: limit } },
                    { "e.e": { $gte: limit } },
                ]
            })
            .then(arr => response.json(arr));
    });

    apiRouter.get("/interactions/filtered/:skip-:limit", function (request, response) {
        db.collection("interactions")
            .find({
                $or: [
                    { e: { $exists: false } },
                    { "e.e": { $gte: limit } },
                    { "e.j": { $gte: limit } },
                    { "e.f": { $gte: limit } },
                    { "e.d": { $gte: limit } },
                    { "e.s": { $gte: limit } },
                    { "e.a": { $gte: limit } },
                    { "e.su": { $gte: limit } },
                    { "e.c": { $gte: limit } },
                    { "e.v": { $gte: limit } },
                    { "e.e": { $gte: limit } },
                ]
            })
            .skip(parseInt(request.params.skip) || 0)
            .limit(parseInt(request.params.limit) || 0)
            .toArray()
            .then(arr => response.json(arr));
    });

    apiRouter.get("/user/:id", function (request, response) {
        db.collection("users")
            .findOne(new ObjectID(request.params.id))
            .then(arr => response.json(arr));
    });

    apiRouter.get("/user/:id/interactions", function (request, response) {
        db.collection("interactions")
            .find({ ui: request.params.id })
            .toArray()
            .then(arr => response.json(arr));
    });

    apiRouter.get("/user/:id/interactions/count", function (request, response) {
        db.collection("interactions")
            .countDocuments({
                ui: request.params.id
            })
            .then(arr => response.json(arr));
    });

    apiRouter.get("/user/:id/interactions/:skip-:limit", function (request, response) {
        db.collection("interactions")
            .find({ ui: request.params.id })
            .skip(parseInt(request.params.skip) || 0)
            .limit(parseInt(request.params.limit) || 0)
            .toArray()
            .then(arr => response.json(arr));
    });

    apiRouter.get("/user/:id/interactions/filtered", function (request, response) {
        db.collection("interactions")
            .find({
                ui: request.params.id,
                $or: [
                    { e: { $exists: false } },
                    { "e.e": { $gte: limit } },
                    { "e.j": { $gte: limit } },
                    { "e.f": { $gte: limit } },
                    { "e.d": { $gte: limit } },
                    { "e.s": { $gte: limit } },
                    { "e.a": { $gte: limit } },
                    { "e.su": { $gte: limit } },
                    { "e.c": { $gte: limit } },
                    { "e.v": { $gte: limit } },
                    { "e.e": { $gte: limit } },
                ]
            })
            .toArray()
            .then(arr => response.json(arr));
    });

    apiRouter.get("/user/:id/interactions/filtered/count", function (request, response) {
        db.collection("interactions")
            .countDocuments({
                ui: request.params.id,
                $or: [
                    { e: { $exists: false } },
                    { "e.e": { $gte: limit } },
                    { "e.j": { $gte: limit } },
                    { "e.f": { $gte: limit } },
                    { "e.d": { $gte: limit } },
                    { "e.s": { $gte: limit } },
                    { "e.a": { $gte: limit } },
                    { "e.su": { $gte: limit } },
                    { "e.c": { $gte: limit } },
                    { "e.v": { $gte: limit } },
                    { "e.e": { $gte: limit } },
                ]
            })
            .then(arr => response.json(arr));
    });

    apiRouter.get("/user/:id/interactions/filtered/:skip-:limit", function (request, response) {
        db.collection("interactions")
            .find({
                ui: request.params.id,
                $or: [
                    { e: { $exists: false } },
                    { "e.e": { $gte: limit } },
                    { "e.j": { $gte: limit } },
                    { "e.f": { $gte: limit } },
                    { "e.d": { $gte: limit } },
                    { "e.s": { $gte: limit } },
                    { "e.a": { $gte: limit } },
                    { "e.su": { $gte: limit } },
                    { "e.c": { $gte: limit } },
                    { "e.v": { $gte: limit } },
                    { "e.e": { $gte: limit } },
                ]
            })
            .skip(parseInt(request.params.skip) || 0)
            .limit(parseInt(request.params.limit) || 0)
            .toArray()
            .then(arr => response.json(arr));
    });

    apiRouter.get("/interaction/:id", function (request, response) {
        db.collection("interactions")
            .findOne(new ObjectID(request.params.id))
            .then(arr => response.json(arr));
    });

    apiRouter.get("/websites", function (request, response) {
        db.collection("websites")
            .aggregate([
                {
                    $project: {
                        _id: false,
                        url: "$_id",
                        count: true,
                        category: true
                    }
                }
            ])
            .toArray()
            .then(arr => response.json(arr));
    });

    return apiRouter;
}
