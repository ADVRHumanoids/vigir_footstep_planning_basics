# 
#  Copyright (C) 2016 IIT-ADVR
#  Author: Dimitrios Kanoulas
#  email: Dimitrios.Kanoulas@iit.it
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with this program. If not, see <http://www.gnu.org/licenses/>
#

cmake_minimum_required(VERSION 2.8.12)
if(COMMAND cmake_policy)
    cmake_policy(SET CMP0003 OLD)
    cmake_policy(SET CMP0005 NEW)
    cmake_policy(SET CMP0017 NEW)
endif(COMMAND cmake_policy)

project(vigir_footstep_planning_basics)

add_subdirectory(vigir_footstep_planning_lib)
add_subdirectory(vigir_footstep_planning_plugins)
add_subdirectory(vigir_footstep_planning_rviz_plugin)
add_subdirectory(vigir_footstep_planning_widgets)
