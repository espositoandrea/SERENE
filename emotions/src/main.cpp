#include <iostream>

#include <opencv/cv.hpp>

#include <PhotoDetector.h>
#include <Frame.h>

#include "utilities.hpp"
#include "base64.hpp"

int main(int argc, char **argv)
{
    std::cout << "Hello World!\n";

    std::string videoPath = "BASE64";
    const bool result = setup_options(argc, argv, videoPath);
    if(!result) return 1;

    const unsigned int nFaces = 1;
    const int faceDetectorMode = (int) affdex::FaceDetectorMode::LARGE_FACES;

//    std::shared_ptr<affdex::Detector> detector;

//    detector = std::make_shared<affdex::PhotoDetector>(nFaces, (affdex::FaceDetectorMode) faceDetectorMode);

//    detector->setDetectAllEmotions(true);
//    detector->setDetectAllExpressions(true);
//    detector->setDetectAllEmojis(true);
//    detector->setDetectAllAppearances(true);
//    detector->setClassifierPath(DATA_FOLDER);
//    detector->setImageListener(listenPtr.get());

//    detector->start();

    //videoPath is of type std::wstring on windows, but std::string on other platforms.
    std::string decoded = base64_decode(videoPath);
    cv::Mat img = cv::imdecode(std::vector<uchar>(decoded.begin(), decoded.end()), cv::IMREAD_UNCHANGED);

    // Create a frame
//    affdex::Frame frame(img.size().width, img.size().height, img.data, affdex::Frame::COLOR_FORMAT::BGR);

//    ((affdex::PhotoDetector *) detector.get())->process(frame); //Process an image

    return 0;
}