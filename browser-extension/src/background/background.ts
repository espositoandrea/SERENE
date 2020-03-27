import collect from "../collector";
import EmotionAnalysis from "../emotion-analysis/emotion-analysis";
import * as Webcam from "webcamjs";


const showStartingSurvey = async () => {
    new Promise<void>(resolve => {
        chrome.runtime.onInstalled.addListener(() => {
            // TODO: Show survey
            console.log("Survey");
            resolve()
        });
    })
};
const showStartingGuide = async () => {
    new Promise<void>(resolve => {
        chrome.runtime.onInstalled.addListener(() => {
            // TODO: Show guide
            console.log("Guide");
            resolve()
        });
    })
};

showStartingSurvey()
    .then(showStartingGuide)
    .then(() => collect());

//EmotionAnalysis.analyzeWebcamPhoto()