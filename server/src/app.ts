import * as express from 'express';
import * as fs from 'fs';
import * as path from 'path';
import * as bodyParser from 'body-parser';
import { MongoClient } from 'mongodb';
import * as cors from 'cors';

import router from './routes';

const app: express.Application = express();
const requestSizeLimit = '50mb';

if (!fs.existsSync('temp')) {
    console.log('Creating temp/ directory');
    fs.mkdirSync('temp');
}

app.use(bodyParser.json({ limit: requestSizeLimit }));
app.use(bodyParser.urlencoded({ limit: requestSizeLimit, extended: false }));
app.use(bodyParser.raw({ limit: requestSizeLimit }));
app.use(cors());

app.use('/assets', express.static('assets'));
app.use('/downloads', express.static('downloads'));

MongoClient.connect(process.env.DB_HOST, { useUnifiedTopology: true }, (err, client) => {
    if (err) return console.log(err);
    const db = client.db(process.env.DB_NAME);

    app.use(router(db));
});

export default app;
