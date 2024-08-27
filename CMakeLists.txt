project(TopLFV)
cmake_minimum_required(VERSION 3.0)

find_package(ROOT REQUIRED COMPONENTS)
include(${ROOT_USE_FILE})
include_directories(${CMAKE_CURRENT_SOURCE_DIR}/include ${ROOT_INCLUDE_DIRS})
add_definitions(${ROOT_CXX_FLAGS})

add_library(TopLFV SHARED src/MyAnalysis.cc src/lepton_candidate.cc src/jet_candidate.cc src/event_candidate.cc src/trigger.cc src/PU_reWeighting.cc src/matrix_method.cc src/common_details.cc src/fastforest_functions.cc src/fastforest.cc)
target_link_libraries(TopLFV ${ROOT_LIBRARIES})

add_executable(RunAll bin/Jobs/2016APV/2016APV_LFVTtScalarU/2016APV_LFVTtScalarU_0_0.C)
set_target_properties(RunAll PROPERTIES RUNTIME_OUTPUT_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR})
target_link_libraries(RunAll TopLFV)
