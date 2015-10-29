cmake_minimum_required (VERSION 2.8)
project (seegurke)

# apply some flags
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11 -Werror -Wall -ferror-limit=20 -g -O0")

# include local headers
include_directories(include)

# list all dependencies
set(SEEGURKE_DEPS
	sfml-system sfml-graphics sfml-window sfml-audio thor
)

# -----------------------------------------------------------------------------
# group sources

set(SEEGURKE_PROTO_SRC
	src/proto/sea.cpp
	src/proto/ship.cpp
	src/proto/main.cpp
)

# -----------------------------------------------------------------------------
# Build debugging game executable

add_executable(seegurke_proto ${SEEGURKE_PROTO_SRC})
target_link_libraries(seegurke_proto ${SEEGURKE_DEPS})
