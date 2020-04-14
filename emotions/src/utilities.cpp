/**
 * \file utilities.cpp
 * \brief Implementation of utilities.hpp.
 *
 * \author Andrea Esposito
 * \date April 8, 2020
 */

#include <iostream>
#include <regex>
#include <fstream>
#include <algorithm>

#include <boost/program_options.hpp>

#include "utilities.hpp"
#include "data_uri.hpp"

exit_codes setup_options(int argc, char **argv, std::vector<std::string> &images)
{
    namespace po = boost::program_options;

    std::string file_path;

    po::options_description options("Available options");
    options.add_options()("help,h", "Display this help message")("file,f", po::value<std::string>(&file_path),
                                                                 "The file containing the images to be analyzed (as a data URI)");

    po::options_description hidden("Hidden options");
    hidden.add_options()("image", po::value<std::vector<std::string>>(&images)->multitoken(),
                         "The image to be analyzed (as a data URI)");

    po::positional_options_description arguments;
    arguments.add("image", -1);

    po::options_description all_options("All options");
    all_options.add(options);
    all_options.add(hidden);

    po::variables_map args = nullptr;
    try
    {
        po::store(po::command_line_parser(argc, argv).options(all_options).positional(arguments).run(), args);
        po::notify(args);

        if (args.count("help"))
        {
            std::cout << "Usage: " << argv[0] << " [options] DATA_URI..." << std::endl;
            std::cout << "  or:  " << argv[0] << " [options] --file FILE" << std::endl;
            std::cout << "Analyze the emotions of an image using Affectiva." << std::endl;
            std::cout << std::endl
                      << options << std::endl;
            return exit_codes::HALT;
        }
        else if (args.count("image") && args.count("file"))
        {
            throw po::error("You cannot specify both a file and an image");
        }
        else if (!args.count("image") && !args.count("file"))
        {
            throw po::error("You must specify at least an image!");
        }

        if (args.count("file"))
        {
            std::ifstream file(file_path, std::ios::in | std::ios::binary);
            std::flush(std::cerr);
            std::string line;
            images.clear();
            while (std::getline(file, line))
            {
                images.push_back(data_uri(line).get_data());
            }
        }
        else
        {
            for (auto &image : images)
            {
                if (data_uri::is_data_uri(image))
                {
                    image = data_uri(image).get_data();
                }
                else
                {
                    std::ifstream file(image, std::ios::in | std::ios::binary);
                    image = std::string(std::istreambuf_iterator<char>(file), std::istreambuf_iterator<char>());

                    if (data_uri::is_data_uri(image))
                    {
                        image = data_uri(image).get_data();
                    }
                    else
                    {
                        throw po::error("A given image is invalid!");
                    }
                }
            }
        }
    }
    catch (po::error &e)
    {
        std::cerr << "ERROR: " << e.what() << std::endl
                  << std::endl;
        std::cerr << "For help, use the -h option." << std::endl
                  << std::endl;
        return exit_codes::ARGUMENT_ERROR;
    }
    catch (...)
    {
        std::cerr << "Unknown error!\n";
        return exit_codes::UNKNOWN_ARGUMENT_ERROR;
    }

    return exit_codes::OK;
}
