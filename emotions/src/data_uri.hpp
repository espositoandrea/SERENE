//
// Created by andrea on 09/04/20.
//

#ifndef EMOTIONS_DATA_URI_HPP
#define EMOTIONS_DATA_URI_HPP

#include <string>

class data_uri
{
private:
    std::string m_type;
    std::string m_data;

public:
    static bool is_data_uri(const std::string &s);

    explicit data_uri(const std::string &s);

    std::string get_type() const;

    std::string get_data() const;

    std::string get_uri() const;

    class string_not_uri : public std::exception
    {
        const char *what() const noexcept override;
    };
};


#endif //EMOTIONS_DATA_URI_HPP
