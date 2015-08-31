#!/usr/bin/env python

import rospy
from TravelAndDetectPeople import TravelAndDetectPeople

from datetime import time, date, timedelta
from dateutil.tz import tzlocal

from strands_executive_msgs.msg import Task
from strands_executive_msgs import task_utils

if __name__ == '__main__':

    rospy.init_node('linda_wander_routine')

    # start and end times -- all times should be in local timezone
    localtz = tzlocal()
    start = time(8,00, tzinfo=localtz)
    end = time(23,00, tzinfo=localtz)

    # how long to stand idle before doing something
    idle_duration=rospy.Duration(3)

    routine = TravelAndDetectPeople(daily_start=start, daily_end=end, idle_duration=idle_duration) 
    #routine = TravelAndDetectPeopleOnDemand(daily_start=start, daily_end=end, idle_duration=idle_duration) 

    routine.create_routine()

    routine.start_routine()

    rospy.spin()
