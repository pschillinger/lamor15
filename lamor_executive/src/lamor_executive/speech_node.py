#!/usr/bin/env python
import rospy

from strands_executive_msgs.msg import Task

from strands_executive_msgs import task_utils

from strands_executive_msgs.srv import AddTasks, DemandTask, SetExecutionStatus

class SpeechNode(object):

	def get_service(self, service_name, service_type):    
		rospy.loginfo('Waiting for %s service...' % service_name)
		rospy.wait_for_service(service_name)
		rospy.loginfo("Done")        
		return rospy.ServiceProxy(service_name, service_type)

	def get_execution_status_service(self):
		return self.get_service('/task_executor/set_execution_status', SetExecutionStatus)

	def get_demand_task_service(self):
		return self.get_service('/task_executor/demand_task', DemandTask)

	def get_add_tasks_service(self):
		return self.get_service('/task_executor/add_tasks', AddTasks)


	def __init__(self):

		set_execution_status = self.get_execution_status_service()
		set_execution_status(True)

		
		waypoints = ['WayPoint%d' % (i + 1) for i in range(4)]
		tasks = []
		for i in range(len(waypoints)):
			task = Task()
			task.action = '/speak'
			task.max_duration = rospy.Duration(15)
			#task.start_node_id = waypoints[i]
			#task.end_node_id = waypoints[i]

			task_utils.add_string_argument(task, 'Hello!')

			task.start_after = rospy.get_rostime() + rospy.Duration(10)
			task.end_before = task.start_after + rospy.Duration(task.max_duration.to_sec() * 8)

			tasks.append(task)

		add_tasks = self.get_add_tasks_service()
		add_tasks(tasks)