import * as express from "express";
import * as bodyParser from "body-parser";
import EmotionAnalysis, {Emotions} from "./emotion-analysis";
import {CollectedData} from "../extension/collector";

interface FinalData extends CollectedData {
    image: string,
    emotions?: Emotions
}

const app = express();
const port = 3000;
const requestSizeLimit = '50mb';

app.use(bodyParser.json({limit: requestSizeLimit}));
app.use(bodyParser.urlencoded({limit: requestSizeLimit, extended: false}));

app.post("/data/store", (request, response) => {
    const data: FinalData[] = JSON.parse(request.body.data);
    data.forEach(async frame => {
        frame.emotions = await EmotionAnalysis.analyzeImage(frame.image);

        // Deleting the webcam image for privacy
        delete frame.image;
    });

    // TODO: Store 'data'
});

app.listen(port, () => {
    console.log(`Listening on port ${port}`);
});
