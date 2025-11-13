cmake_minimum_required(VERSION 3.16)

project(derrpy LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_executable(derrpy main.cpp
    dataerr.h dataerr.cpp
    unit.h unit.cpp
)

include(GNUInstallDirs)
install(TARGETS derrpy
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
    RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
)
