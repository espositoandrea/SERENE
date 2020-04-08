//
// Created by andrea on 08/04/20.
//

#ifndef EMOTIONS_UTILITIES_CPP
#define EMOTIONS_UTILITIES_CPP

#include <iostream>

#include <boost/program_options.hpp>

#include "utilities.hpp"

bool setup_options(int argc, char **argv,
                   std::string &image)
{
    namespace po = boost::program_options;

    po::options_description description("Analyze the emotions of an image using Affectiva");
    description.add_options()
            ("help,h", "Display this help message")
            ("image,i", po::value<std::string>(&image)->required(), "The image to be analyzed (as a data URI)");
    po::variables_map args = nullptr;
    try
    {
        po::store(po::parse_command_line(argc, argv, description), args);
        po::notify(args);

        if (args.count("help"))
        {
            std::cout << description << "\n";
            return false;
        }
    }
    catch (po::error &e)
    {
        std::cerr << "ERROR: " << e.what() << std::endl << std::endl;
        std::cerr << "For help, use the -h option." << std::endl << std::endl;
        return false;
    }
    catch (...)
    {
        std::cerr << "Unknown error!\n";
        return false;
    }

    return true;
}

#endif //EMOTIONS_UTILITIES_CPP
