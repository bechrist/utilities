/* vector_utils.hpp Test Suite */
#include <vector>
#include <cmath>

#include "logger.hpp"
#include "vector_utils.hpp"

#define BOOST_TEST_MODULE "Vector Utilities"
#include <boost/test/unit_test.hpp>

BOOST_AUTO_TEST_CASE(inf_norm) {
    std::vector<double> v1 = {-1,5.3,-7,0.4};
    std::vector<double> v2 = {-1,5.3,7,0.4};

    BOOST_CHECK(norm(v1, "inf") == 7);
    BOOST_CHECK(norm(v2, "inf") == 7);
}