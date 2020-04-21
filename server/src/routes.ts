import { Router } from 'express';
import DataProcessor from './data-processor';
import survey from './survey-data';
import * as path from 'path';

export default function router(db) {
    const router = Router();

    router.get('/', (req, res) => res.sendFile(path.resolve('./index.html')));

    router.get('/survey', (req, res) => res.sendFile(path.resolve('./survey.html')));

    router.post("/data/store", async (request, response) => {
        const data = JSON.parse(request.body.data);
        // Data received: notify the sender
        response.send({ done: true, errors: null });

        DataProcessor.process(data)
            .then((data) => {
                db.collection('interactions').insertMany(data, (err, result) => {
                    if (err) {
                        // TODO: There was an error in writing to the DB: handle this error
                        return console.log(err);
                    }

                    console.log('saved to database');
                });
            });
    });

    router.post("/survey/store", (request, response) => {
        let userData = request.body;

        db.collection('users').insertOne(userData, (err, result) => {
            if (err) {
                // TODO: There was an error in writing to the DB: handle this error
                response.json({ done: false, errors: err });
                return console.log(err);
            }

            response.json({ done: true, errors: [], userId: result.insertedId });
        });
    });

    return router;
}
