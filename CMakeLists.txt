project(TopLFV)
cmake_minimum_required(VERSION 3.0)

list(APPEND CMAKE_PREFIX_PATH "/Users/jingyan/root")
find_package(ROOT REQUIRED COMPONENTS)
include(${ROOT_USE_FILE})
include_directories(${CMAKE_CURRENT_SOURCE_DIR}/include ${ROOT_INCLUDE_DIRS})
add_definitions(${ROOT_CXX_FLAGS})

add_library(TopLFV SHARED src/MyAnalysis.cc src/lepton_candidate.cc src/jet_candidate.cc src/event_candidate.cc src/trigger.cc src/PU_reWeighting.cc)
target_link_libraries(TopLFV ${ROOT_LIBRARIES})

add_executable(RunAll src/main.cc)
set_target_properties(RunAll PROPERTIES RUNTIME_OUTPUT_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR})
target_link_libraries(RunAll TopLFV)
