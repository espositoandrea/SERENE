#include <iostream>

#include <opencv2/highgui/highgui.hpp>
#include <opencv2/core/core.hpp>
#include <opencv/cv.hpp>

#include <PhotoDetector.h>
#include <Frame.h>

#include "common/PlottingImageListener.hpp"
#include "common/StatusListener.hpp"

#include "exit_codes.hpp"
#include "utilities.hpp"
#include "base64.hpp"

int main(int argc, char **argv)
{
    std::vector <std::string> images;
    const exit_codes result = setup_options(argc, argv, images);
    if (result != exit_codes::OK) return static_cast<int>(result);

    const unsigned int nFaces = 1;
    const int faceDetectorMode = (int) affdex::FaceDetectorMode::LARGE_FACES;

    std::shared_ptr <affdex::Detector> detector = std::make_shared<affdex::PhotoDetector>(nFaces,
                                                                                          (affdex::FaceDetectorMode) faceDetectorMode);

    std::shared_ptr <PlottingImageListener> listenPtr(new PlottingImageListener());

    detector->setDetectAllEmotions(true);
    detector->setDetectAllExpressions(true);
    detector->setDetectAllEmojis(true);
    detector->setDetectAllAppearances(true);
    detector->setClassifierPath(affdex::path("/home/andrea/Desktop/affdex-sdk/data/"));
    detector->setImageListener(listenPtr.get());

    detector->start();

    std::shared_ptr <StatusListener> videoListenPtr = std::make_shared<StatusListener>();
    detector->setProcessStatusListener(videoListenPtr.get());

    for (const auto &image : images)
    {
        std::string decoded = base64_decode(image);
        cv::Mat img = cv::imdecode(std::vector<uchar>(decoded.begin(), decoded.end()), cv::IMREAD_UNCHANGED);

        affdex::Frame frame(img.size().width, img.size().height, img.data, affdex::Frame::COLOR_FORMAT::BGR);

        ((affdex::PhotoDetector *) detector.get())->process(frame); //Process an image

        do
        {
            if (listenPtr->getDataSize() > 0)
            {
                std::pair <Frame, std::map<FaceId, Face>> dataPoint = listenPtr->getData();
                affdex::Frame frame = dataPoint.first;
                std::map <FaceId, Face> faces = dataPoint.second;

                listenPtr->addResult(faces, frame.getTimestamp());
            }
        } while ((videoListenPtr->isRunning() || listenPtr->getDataSize() > 0));
    }

    listenPtr->outputToFile(std::cout);
    return 0;
}
