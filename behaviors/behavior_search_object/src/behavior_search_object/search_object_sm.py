#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_search_object')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, Logger
from lamor_flexbe_states.metric_sweep_state import MetricSweepState
from lamor_flexbe_states.recognize_object_state import RecognizeObjectState
from lamor_flexbe_states.speech_output_state import SpeechOutputState
from lamor_flexbe_states.store_pointcloud_state import StorePointcloudState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Sat Aug 29 2015
@author: Philipp Schillinger
'''
class SearchObjectSM(Behavior):
	'''
	Looks for an object at the current waypoint.
	'''


	def __init__(self):
		super(SearchObjectSM, self).__init__()
		self.name = 'Search Object'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		pcl_topic = '/local_metric_map/metaroom'
		object_name = 'teabox'
		# x:183 y:440, x:383 y:190
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
		_state_machine.userdata.text_found = 'I found %s' % object_name
		_state_machine.userdata.text_not_found = 'I will continue my search'

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:47 y:28
			OperatableStateMachine.add('Perform_Sweep',
										MetricSweepState(sweep_type=MetricSweepState.SHORT),
										transitions={'sweeped': 'Store_Pointcloud', 'failed': 'failed'},
										autonomy={'sweeped': Autonomy.Off, 'failed': Autonomy.Off})

			# x:38 y:228
			OperatableStateMachine.add('Recognize_Object',
										RecognizeObjectState(object_name=object_name),
										transitions={'detected': 'Say_Found', 'not_detected': 'Say_Not_Found', 'failed': 'failed'},
										autonomy={'detected': Autonomy.Low, 'not_detected': Autonomy.Low, 'failed': Autonomy.Full},
										remapping={'pointcloud': 'pointcloud'})

			# x:44 y:328
			OperatableStateMachine.add('Say_Found',
										SpeechOutputState(),
										transitions={'done': 'finished', 'failed': 'failed'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Full},
										remapping={'text': 'text_found'})

			# x:244 y:278
			OperatableStateMachine.add('Say_Not_Found',
										SpeechOutputState(),
										transitions={'done': 'finished', 'failed': 'failed'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Full},
										remapping={'text': 'text_not_found'})

			# x:41 y:128
			OperatableStateMachine.add('Store_Pointcloud',
										StorePointcloudState(topic=pcl_topic),
										transitions={'done': 'Recognize_Object'},
										autonomy={'done': Autonomy.Off},
										remapping={'pointcloud': 'pointcloud'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
