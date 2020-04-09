//
// Created by andrea on 09/04/20.
//

#include "data_uri.hpp"

const std::string PROTOCOL = "data:", BASE64 = ";base64,";

bool data_uri::is_data_uri(const std::string &s)
{
    return s.find(PROTOCOL) == 0 && s.find(BASE64) != std::string::npos;
}

data_uri::data_uri(const std::string &s)
{
    if (!data_uri::is_data_uri(s)) throw data_uri::string_not_uri();

    std::size_t base64_position = s.find(BASE64);

    m_type = s.substr(PROTOCOL.size(), base64_position - PROTOCOL.size());
    m_data = s.substr(PROTOCOL.size() + m_type.size() + BASE64.size());
}

std::string data_uri::get_type() const
{
    return m_type;
}

std::string data_uri::get_data() const
{
    return m_data;
}

std::string data_uri::get_uri() const
{
    return PROTOCOL + m_type + BASE64 + m_data;
}

const char *data_uri::string_not_uri::what() const noexcept
{
    return "The given string isn't a Data URI";
}
