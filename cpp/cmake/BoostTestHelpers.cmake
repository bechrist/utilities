#[[BoostTestHelpers.cmake - Driving Boost.Test with CMake

MIT License

Copyright (c) [2015] [Eric Scott Barr]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
]]

function(add_boost_test SOURCE_FILE_NAME)
        get_filename_component(TEST_EXECUTABLE_NAME ${SOURCE_FILE_NAME} NAME_WE)

        add_executable(${TEST_EXECUTABLE_NAME} ${SOURCE_FILE_NAME})
        target_link_libraries(${TEST_EXECUTABLE_NAME}
                ${PROJECT_NAME_STR}_test
                ${Boost_LIBRARIES} 
                boost_matheval_x3
                ${HDF5_CXX_LIBRARIES}
        )

        target_include_directories(${TEST_EXECUTABLE_NAME}
                PRIVATE ${boost_matheval_INCLUDE_DIRS}
        )

        file(READ "${SOURCE_FILE_NAME}" SOURCE_FILE_CONTENTS)
        string(
                REGEX MATCHALL "BOOST_AUTO_TEST_CASE\\( *([A-Za-z_0-9]+) *\\)" 
                FOUND_TESTS ${SOURCE_FILE_CONTENTS}
        )

        foreach(HIT ${FOUND_TESTS})
                string(
                        REGEX REPLACE ".*\\( *([A-Za-z_0-9]+) *\\).*" "\\1" TEST_NAME ${HIT}
                )

                if( (${TEST_NAME} STREQUAL "config_1_gmres_4") AND (NOT PETSC_FOUND) ) 
                        continue()
                endif()

                add_test(
                        NAME "${TEST_EXECUTABLE_NAME}.${TEST_NAME}" 
                        COMMAND ${TEST_EXECUTABLE_NAME}
                        --run_test=${TEST_NAME} 
                        --catch_system_error=yes
                        --log_level=message
                )
        endforeach()
endfunction()