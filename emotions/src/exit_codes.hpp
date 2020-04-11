/**
 * \file exit_codes.hpp
 * \brief An header to define the exit codes of the tool.
 *
 * This header contains the definition of all the exit codes of the tool
 *
 * \author Andrea Esposito
 * \date April 10, 2020
 */

#ifndef EMOTIONS_EXIT_CODES_HPP
#define EMOTIONS_EXIT_CODES_HPP

/**
 * \brief A collection of all the exit codes of the tool.
 *
 * This enum contains all the (expected) exit codes of the tool.
 */
enum class exit_codes : int
{
    OK = 0, ///< The tool exited with no error completing its tasks.
    HALT = 1, ///< The tool exited with no error, but without completing its tasks.
    ARGUMENT_ERROR = 2, ///< The tool exited due to errors in the given arguments.
    UNKNOWN_ARGUMENT_ERROR = 3 ///< The tool exited due to unknown errors while parsing the arguments.
};

#endif //EMOTIONS_EXIT_CODES_HPP
