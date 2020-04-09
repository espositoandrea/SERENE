#include <iostream>

#include <opencv2/highgui/highgui.hpp>
#include <opencv2/core/core.hpp>
#include <opencv/cv.hpp>

#include <PhotoDetector.h>
#include <Frame.h>

#include "common/PlottingImageListener.hpp"
#include "common/StatusListener.hpp"

#include "utilities.hpp"
#include "base64.hpp"

int main(int argc, char **argv)
{
    // std::cout << "Hello World!\n";

    std::string videoPath = "BASE64";
    const bool result = setup_options(argc, argv, videoPath);
    if (!result) return 1;

    const unsigned int nFaces = 1;
    const int faceDetectorMode = (int) affdex::FaceDetectorMode::LARGE_FACES;

    std::shared_ptr<affdex::Detector> detector  = std::make_shared<affdex::PhotoDetector>(nFaces, (affdex::FaceDetectorMode) faceDetectorMode);

    std::shared_ptr<PlottingImageListener> listenPtr(new PlottingImageListener(std::cout, false));

    detector->setDetectAllEmotions(true);
    detector->setDetectAllExpressions(true);
    detector->setDetectAllEmojis(true);
    detector->setDetectAllAppearances(true);
    detector->setClassifierPath(affdex::path("/home/andrea/Desktop/affdex-sdk/data/"));
    detector->setImageListener(listenPtr.get());

    detector->start();

    std::shared_ptr<StatusListener> videoListenPtr = std::make_shared<StatusListener>();
    detector->setProcessStatusListener(videoListenPtr.get());

    //videoPath is of type std::wstring on windows, but std::string on other platforms.

    std::string decoded = base64_decode(videoPath);
    cv::Mat img = cv::imdecode(std::vector<uchar>(decoded.begin(), decoded.end()), cv::IMREAD_UNCHANGED);

    // Create a frame
    affdex::Frame frame(img.size().width, img.size().height, img.data, affdex::Frame::COLOR_FORMAT::BGR);

    ((affdex::PhotoDetector *) detector.get())->process(frame); //Process an image

    do
    {
        if (listenPtr->getDataSize() > 0)
        {
            std::pair<Frame, std::map<FaceId, Face> > dataPoint = listenPtr->getData();
            affdex::Frame frame = dataPoint.first;
            std::map<FaceId, Face> faces = dataPoint.second;


            if (false)
            {
                listenPtr->draw(faces, frame);
            }

            std::cerr << "timestamp: " << frame.getTimestamp()
                      << " cfps: " << listenPtr->getCaptureFrameRate()
                      << " pfps: " << listenPtr->getProcessingFrameRate()
                      << " faces: "<< faces.size() << std::endl;

            listenPtr->outputToFile(faces, frame.getTimestamp());
        }
    } while ((videoListenPtr->isRunning() || listenPtr->getDataSize() > 0));

    return 0;
}
