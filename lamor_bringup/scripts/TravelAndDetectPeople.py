#!/usr/bin/env python

import rospy

from std_msgs.msg import String
from strands_executive_msgs import task_utils
from strands_executive_msgs.msg import Task
from strands_navigation_msgs.msg import TopologicalMap
from strands_navigation_msgs.srv import EstimateTravelTime
from mongodb_store_msgs.msg import StringList
from mongodb_store.message_store import MessageStoreProxy

from datetime import time, date, timedelta
from dateutil.tz import tzlocal

from routine_behaviours.robot_routine import RobotRoutine

import random

class TravelAndDetectPeople(RobotRoutine):
    """ Creates a routine which simply visits nodes. """

    def __init__(self, daily_start, daily_end, idle_duration=rospy.Duration(5), charging_point = 'ChargingPoint'):     
        RobotRoutine.__init__(self, daily_start, daily_end, idle_duration=idle_duration, charging_point=charging_point)
        self.node_names = set()  
	self.current_node = None
	self.closest_node = None      
        self.topological_map = None
	self.current_node_msg = None
	self.closest_node_msg = None
        self.random_nodes = []
        rospy.Subscriber('topological_map', TopologicalMap, self.map_callback)
	rospy.Subscriber('current_node', String, self.current_node_callback)
	rospy.Subscriber('closest_node', String, self.closest_node_callback)
   
    def map_callback(self, msg):        
        print 'got map: %s' % len(msg.nodes)
        self.topological_map = msg
        self.node_names = set([node.name for node in msg.nodes if node.name != 'ChargingPoint'])
        if len(self.random_nodes) == 0:
            self.random_nodes = list(self.node_names)

    def current_node_callback(self,msg):
	self.current_node_msg = msg
	self.current_node = msg.data

    def closest_node_callback(self,msg):
	self.closest_node_msg = msg
	self.closest_node = msg.data	

    def get_nodes(self):
        while len(self.node_names) == 0:
            print 'no nodes'
            rospy.sleep(1)
        return self.node_names

    def get_current_node(self):
        return self.current_node

    def get_closest_node(self):
        return self.closest_node

    def get_best_node(self):
	#cn = self.get_current_node()
        #if not cn:
	return self.get_closest_node()
	#return self.get_current_node()

    def all_waypoints(self):
        return self.get_nodes()

    def all_waypoints_except(self, exceptions = []):
        return self.all_waypoints() - set(exceptions)


    def max_single_trip_time(self, waypoints):

        expected_time = rospy.ServiceProxy('topological_navigation/travel_time_estimator', EstimateTravelTime)        

        max_time = rospy.Duration(0)
        for start in waypoints:
            for end in waypoints:
                if start != end:
                    et = expected_time(start=start, target=end).travel_time
                    if et > max_time:
                        max_time = et

        return max_time

    def create_detection_routine(self, waypoints=None, daily_start=None, daily_end=None, repeat_delta=None):
	pass
        #tasks = self.create_interaction_task()
	#repeat_delta = timedelta(minutes=1)
        #self.create_task_routine(tasks=[tasks], daily_start=daily_start, daily_end=daily_end, repeat_delta=repeat_delta)

    def create_routine(self):
        
        self.create_detection_routine()

    def on_idle(self):
        """
            Called when the routine is idle. Default is to trigger travel to the charging. As idleness is determined by the current schedule, if this call doesn't utlimately cause a task schedule to be generated this will be called repeatedly.
        """

        nearby_nodes = self.find_nearby_nodes()

        rospy.loginfo('Idle for too long, generating a random waypoint task')
        self.add_tasks([self.create_travel_task(random.choice(nearby_nodes))])
    
    def create_travel_task(self, waypoint_name, max_duration=rospy.Duration(120)):
	# Task: robot travels to waypoint
	# 
	task = Task()
	task.action = '/flexbe/execute_behavior'
	task_utils.add_string_argument(task,'Tell Random Joke')
	task.max_duration = max_duration
	task.start_node_id = waypoint_name
	task.end_node_id = waypoint_name
        return task

    def create_interaction_task(self, waypoint_name, max_duration=rospy.Duration(120)):
	# Task: robot detects human and interacts
	task = Task()
	task.action = '/flexbe/execute_behavior'
	task_utils.add_string_argument(task,'Tell Random Joke')
	task.max_duration = max_duration
	task.start_node_id = waypoint_name
	task.end_node_id = waypoint_name
        return task

    def find_nearby_nodes(self, waypoints=None):

        if not waypoints: 
            waypoints = self.get_nodes()

	# need currpos
	currpos = self.get_best_node()

        expected_time = rospy.ServiceProxy('topological_navigation/travel_time_estimator', EstimateTravelTime)        

	num = 10
        times = []

        for node in waypoints:
		if node != currpos and node != 'ChargingPoint' and node != 'Station':
		    et = expected_time(start=currpos, target=node).travel_time
		    times.append((et.to_sec(),node))

	times.sort()
	nearby_nodes =  [seq[1] for seq in times[:num] ]
        return nearby_nodes

