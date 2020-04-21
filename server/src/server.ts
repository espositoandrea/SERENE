import { config } from 'dotenv';
config();
import * as https from 'https';
import * as http from 'http';
import * as fs from 'fs';

import app from './app';

const hasHTTPS = Boolean(process.env.HTTPS_CERT_KEY && process.env.HTTPS_CERT);
const server = hasHTTPS ? https.createServer({
    key: fs.readFileSync(process.env.HTTPS_CERT_KEY),
    cert: fs.readFileSync(process.env.HTTPS_CERT)
}, app) : http.createServer(app);

server.listen(process.env.PORT, () => {
    console.log(`Listening (HTTP${hasHTTPS ? 'S' : ''}) on port ${process.env.PORT}`);
});
