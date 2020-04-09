
/**
 * @author Affectiva, heavily modified by Andrea Esposito.
 */

#ifndef PLOTTING_IMAGE_LISTENERS_HPP
#define PLOTTING_IMAGE_LISTENERS_HPP


#include <iostream>
#include <memory>
#include <chrono>
#include <thread>
#include <mutex>
#include <fstream>
#include <boost/filesystem.hpp>
#include <boost/timer/timer.hpp>

#include <rapidjson/stringbuffer.h>
#include <rapidjson/writer.h>

#include "Visualizer.h"
#include "ImageListener.h"

using namespace affdex;

class PlottingImageListener : public ImageListener
{

    std::mutex mMutex;
    std::deque<std::pair<Frame, std::map<FaceId, Face> > > mDataArray;

    double mCaptureLastTS;
    double mCaptureFPS;
    double mProcessLastTS;
    double mProcessFPS;
    std::ostream &fStream;
    std::chrono::time_point<std::chrono::system_clock> mStartT;
    const bool mDrawDisplay;
    const int spacing = 20;
    const float font_size = 0.5f;
    const int font = cv::FONT_HERSHEY_COMPLEX_SMALL;
    Visualizer viz;

public:


    PlottingImageListener(std::ostream &csv, const bool draw_display)
            : fStream(csv), mDrawDisplay(draw_display), mStartT(std::chrono::system_clock::now()),
              mCaptureLastTS(-1.0f), mCaptureFPS(-1.0f),
              mProcessLastTS(-1.0f), mProcessFPS(-1.0f)
    {
    }

    cv::Point2f minPoint(VecFeaturePoint points)
    {
        VecFeaturePoint::iterator it = points.begin();
        FeaturePoint ret = *it;
        for (; it != points.end(); it++)
        {
            if (it->x < ret.x) ret.x = it->x;
            if (it->y < ret.y) ret.y = it->y;
        }
        return cv::Point2f(ret.x, ret.y);
    };

    cv::Point2f maxPoint(VecFeaturePoint points)
    {
        VecFeaturePoint::iterator it = points.begin();
        FeaturePoint ret = *it;
        for (; it != points.end(); it++)
        {
            if (it->x > ret.x) ret.x = it->x;
            if (it->y > ret.y) ret.y = it->y;
        }
        return cv::Point2f(ret.x, ret.y);
    };


    double getProcessingFrameRate()
    {
        std::lock_guard<std::mutex> lg(mMutex);
        return mProcessFPS;
    }

    double getCaptureFrameRate()
    {
        std::lock_guard<std::mutex> lg(mMutex);
        return mCaptureFPS;
    }

    int getDataSize()
    {
        std::lock_guard<std::mutex> lg(mMutex);
        return mDataArray.size();

    }

    std::pair<Frame, std::map<FaceId, Face>> getData()
    {
        std::lock_guard<std::mutex> lg(mMutex);
        std::pair<Frame, std::map<FaceId, Face>> dpoint = mDataArray.front();
        mDataArray.pop_front();
        return dpoint;
    }

    void onImageResults(std::map<FaceId, Face> faces, Frame image) override
    {
        std::lock_guard<std::mutex> lg(mMutex);
        mDataArray.push_back(std::pair<Frame, std::map<FaceId, Face>>(image, faces));
        std::chrono::time_point<std::chrono::system_clock> now = std::chrono::system_clock::now();
        std::chrono::milliseconds milliseconds = std::chrono::duration_cast<std::chrono::milliseconds>(now - mStartT);
        double seconds = milliseconds.count() / 1000.f;
        mProcessFPS = 1.0f / (seconds - mProcessLastTS);
        mProcessLastTS = seconds;
    };

    void onImageCapture(Frame image) override
    {
        std::lock_guard<std::mutex> lg(mMutex);
        mCaptureFPS = 1.0f / (image.getTimestamp() - mCaptureLastTS);
        mCaptureLastTS = image.getTimestamp();
    };

    static void printFeatures(rapidjson::Writer<rapidjson::StringBuffer> &w, float *features, const char *key,
                              const std::vector<std::string> &viz)
    {
        w.Key(key);
        w.StartObject();
        for (const std::string &property : viz)
        {
            w.Key(property.c_str());
            w.Double(*features);
            features++;
        }
        w.EndObject();
    }

    void outputToFile(const std::map<FaceId, Face> &faces, const double timeStamp)
    {
        rapidjson::StringBuffer s;
        rapidjson::Writer<rapidjson::StringBuffer> w(s);
        w.StartObject();
//        if (faces.empty())
//        {
//            fStream << timeStamp << ",nan,nan,no,unknown,unknown,unknown,unknown,";
//            for (std::string angle : viz.HEAD_ANGLES) fStream << "nan,";
//            for (std::string emotion : viz.EMOTIONS) fStream << "nan,";
//            for (std::string expression : viz.EXPRESSIONS) fStream << "nan,";
//            for (std::string emoji : viz.EMOJIS) fStream << "nan,";
//            fStream << std::endl;
//        }
        for (auto &face_id_pair : faces)
        {
            Face f = face_id_pair.second;

            w.Key("faceId");
            w.Uint(f.id);
            w.Key("dominantEmoji");
            w.String(affdex::EmojiToString(f.emojis.dominantEmoji).c_str());

            w.Key("measurements");
            w.StartObject();
            w.Key("interocularDistance");
            w.Double(f.measurements.interocularDistance);
            printFeatures(w, (float *) &f.measurements.orientation, "orientation", viz.HEAD_ANGLES);
            w.EndObject();

            w.Key("appearance");
            w.StartObject();
            w.Key("glasses");
            w.Bool(f.appearance.glasses == affdex::Glasses::Yes);
            w.Key("age");
            w.String(viz.AGE_MAP[f.appearance.age].c_str());
            w.Key("ethnicity");
            w.String(viz.ETHNICITY_MAP[f.appearance.ethnicity].c_str());
            w.Key("gender");
            w.String(viz.GENDER_MAP[f.appearance.gender].c_str());
            w.EndObject();

            printFeatures(w, (float *) &f.emotions, "emotions", viz.EMOTIONS);
            printFeatures(w, (float *) &f.emotions, "expressions", viz.EXPRESSIONS);
            printFeatures(w, (float *) &f.emojis, "emojis", viz.EMOJIS);
        }
        w.EndObject();
        fStream << s.GetString() << std::endl;
    }

    std::vector<cv::Point2f> CalculateBoundingBox(VecFeaturePoint points)
    {

        std::vector<cv::Point2f> ret;

        //Top Left
        ret.push_back(minPoint(points));

        //Bottom Right
        ret.push_back(maxPoint(points));

        //Top Right
        ret.push_back(cv::Point2f(ret[1].x,
                                  ret[0].y));
        //Bottom Left
        ret.push_back(cv::Point2f(ret[0].x,
                                  ret[1].y));

        return ret;
    }

    void draw(const std::map<FaceId, Face> faces, Frame image)
    {

        const int left_margin = 30;

        cv::Scalar clr = cv::Scalar(0, 0, 255);
        cv::Scalar header_clr = cv::Scalar(255, 0, 0);

        std::shared_ptr<unsigned char> imgdata = image.getBGRByteArray();
        cv::Mat img = cv::Mat(image.getHeight(), image.getWidth(), CV_8UC3, imgdata.get());
        viz.updateImage(img);

        for (auto &face_id_pair : faces)
        {
            Face f = face_id_pair.second;
            VecFeaturePoint points = f.featurePoints;
            std::vector<cv::Point2f> bounding_box = CalculateBoundingBox(points);

            // Draw Facial Landmarks Points
            //viz.drawPoints(points);

            // Draw bounding box
            viz.drawBoundingBox(bounding_box[0], bounding_box[1], f.emotions.valence);

            // Draw a face on screen
            viz.drawFaceMetrics(f, bounding_box);
        }

        viz.showImage();
        std::lock_guard<std::mutex> lg(mMutex);
    }

};

#endif
