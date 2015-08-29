#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('vigir_behavior_sweep_test_behavior')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, Logger
from lamor_flexbe_states.metric_sweep_state import MetricSweepState
from flexbe_states.log_state import LogState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Fri Aug 28 2015
@author: Philipp Schillinger
'''
class SweepTestBehaviorSM(Behavior):
	'''
	Performs a short sweep and logs some stuff.
	'''


	def __init__(self):
		super(SweepTestBehaviorSM, self).__init__()
		self.name = 'Sweep Test Behavior'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:83 y:340, x:283 y:190
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:60 y:78
			OperatableStateMachine.add('Log_Sweep',
										LogState(text='Now performing a short sweep...', severity=Logger.REPORT_INFO),
										transitions={'done': 'Perform_Sweep'},
										autonomy={'done': Autonomy.Off})

			# x:47 y:178
			OperatableStateMachine.add('Perform_Sweep',
										MetricSweepState(sweep_type='short'),
										transitions={'sweeped': 'finished', 'failed': 'failed'},
										autonomy={'sweeped': Autonomy.Off, 'failed': Autonomy.Off})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
