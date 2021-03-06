cmake_minimum_required(VERSION 2.8.3)
project(map_db)

find_package(catkin REQUIRED COMPONENTS
  roscpp
  gnss
  std_msgs
  visualization_msgs
  geometry_msgs
  message_generation
)

set(CMAKE_CXX_FLAGS "-std=c++0x -O2 -Wall -Wno-unused-result ${CMAKE_CXX_FLAGS}")

add_message_files(
  FILES
  AreaClass.msg
  AreaClassArray.msg
  BoxClass.msg
  BoxClassArray.msg
  CrossRoad.msg
  CrossRoadArray.msg
  CrossWalk.msg
  CrossWalkArray.msg
  Curb.msg
  CurbArray.msg
  DTLane.msg
  DTLaneArray.msg
  GuardRail.msg
  GuardRailArray.msg
  Gutter.msg
  GutterArray.msg
  Lane.msg
  LaneArray.msg
  LineClass.msg
  LineClassArray.msg
  Node.msg
  NodeArray.msg
  PointClass.msg
  PointClassArray.msg
  Pole.msg
  PoleArray.msg
  PoleClass.msg
  PoleClassArray.msg
  RoadEdge.msg
  RoadEdgeArray.msg
  RoadMark.msg
  RoadMarkArray.msg
  RoadSign.msg
  RoadSignArray.msg
  SideWalk.msg
  SideWalkArray.msg
  Signal.msg
  SignalArray.msg
  StopLine.msg
  StopLineArray.msg
  StreetLight.msg
  StreetLightArray.msg
  UtilityPole.msg
  UtilityPoleArray.msg
  VectorClass.msg
  VectorClassArray.msg
  WhiteLine.msg
  WhiteLineArray.msg
  ZebraZone.msg
  ZebraZoneArray.msg
)

generate_messages(
  DEPENDENCIES
  std_msgs
)

catkin_package(
#  INCLUDE_DIRS include
#  LIBRARIES fake_drivers
#  CATKIN_DEPENDS other_catkin_pkg
#  DEPENDS system_lib
   DEPENDS gnss
)

###########
## Build ##
###########

include_directories(
  include
  ${catkin_INCLUDE_DIRS}
  /usr/include/pcl-1.7
  /usr/include/eigen3)

add_library(map_db
  lib/map_db/GetFile.cpp
)

add_executable(points_map_query nodes/points_map_query/points_map_query.cpp)
target_link_libraries(points_map_query ${catkin_LIBRARIES} pcl_io map_db)

add_executable(vector_map_query
  nodes/vector_map_query/vector_map_query.cpp
  nodes/vector_map_query/pack_into.cpp)
target_link_libraries(vector_map_query ${catkin_LIBRARIES} map_db)
add_dependencies(vector_map_query map_file_generate_messages_cpp)
