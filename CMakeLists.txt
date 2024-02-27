cmake_minimum_required(VERSION 3.9 FATAL_ERROR)
project(PP)
if(NOT TARGET Garfield::Garfield)
  find_package(Garfield REQUIRED)
endif()
# ---Build executable--------------------------------------------------------   
add_executable(filedlines TPC.cc)
target_link_libraries(fieldlines Garfield::Garfield)
# ---Copy all files locally to the build directory---------------------------   
foreach(_file TPC/mesh.header TPC/mesh.elements TPC/mesh.nodes TPC/dielectrics.dat TPC/TPC.result)
  configure_file(${_file} ${_file} COPYONLY)
endforeach()
