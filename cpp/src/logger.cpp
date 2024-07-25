/* logger.cpp - Logging Setup */
// Modified from: https://gist.github.com/jondeaton/dd0efc6ffaae72e609c2dc8766157ef2
#include <map>
#include <iostream>

#include "logger.hpp"

namespace logger{
    logging::sources::severity_logger<logging::trivial::severity_level> log;

    int level = 2;

    void init() {
        logging::add_common_attributes();

        std::map<int, logging::trivial::severity_level> level_map = {
            {0, logging::trivial::trace},
            {1, logging::trivial::debug},
            {2, logging::trivial::info},
            {3, logging::trivial::warning},
            {4, logging::trivial::error},
            {5, logging::trivial::fatal}
        };

        logging::core::get()->set_filter(
            logging::trivial::severity >= level_map.at(logger::level));

        auto fmtSeverity = logging::expressions::
            attr<logging::trivial::severity_level>("Severity");

        logging::formatter logFmt = 
            logging::expressions::format("[%1%] %2%")
                % fmtSeverity
                % logging::expressions::smessage;

        auto console_sink = logging::add_console_log(std::clog);
        console_sink->set_formatter(logFmt);
    }

    void init(int level) {
        logger::level = level;
        logger::init();
    }
}