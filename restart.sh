#!/bin/bash
cd ../..
catkin_make
cd -
rosrun vision test.py
