/* logger.cpp Header File */
#ifndef LOGGER_HPP
#define LOGGER_HPP

#ifndef BOOST_ALL_DYN_LINK
#define BOOST_ALL_DYN_LINK
#endif

#include <boost/log/trivial.hpp>
#include <boost/log/expressions.hpp>
#include <boost/log/utility/setup.hpp>

namespace logging = boost::log;

#define LOG_TRACE   BOOST_LOG_SEV(logger::log, logging::trivial::trace)
#define LOG_DEBUG   BOOST_LOG_SEV(logger::log, logging::trivial::debug)
#define LOG_INFO    BOOST_LOG_SEV(logger::log, logging::trivial::info)
#define LOG_WARNING BOOST_LOG_SEV(logger::log, logging::trivial::warning)
#define LOG_ERROR   BOOST_LOG_SEV(logger::log, logging::trivial::error)
#define LOG_FATAL   BOOST_LOG_SEV(logger::log, logging::trivial::fatal)

namespace logger {
    extern
        logging::sources::severity_logger<logging::trivial::severity_level> log;

    extern int level;

    void init();
    void init(int level); 
}

#endif 