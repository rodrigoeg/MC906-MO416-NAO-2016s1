cmake_minimum_required(VERSION 3.5)
project(naoClient)

include_directories(vrep-api/include
        vrep-api/remoteApi)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -pthread")
add_compile_options(-DNON_MATLAB_PARSING
        -DMAX_EXT_API_CONNECTIONS=255)

if (UNIX)
    add_compile_options(-D__linux)
else ()
    add_compile_options(-D__APPLE__)
endif ()

set(SOURCE_FILES
        vrep-api/remoteApi/extApi.c
        vrep-api/remoteApi/extApiPlatform.c
        main.cpp
        nao.cpp)

add_executable(naoClient ${SOURCE_FILES})