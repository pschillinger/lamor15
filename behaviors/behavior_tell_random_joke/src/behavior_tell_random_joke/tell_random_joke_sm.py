#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_tell_random_joke')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, Logger
from lamor_flexbe_states.pick_joke_state import PickJokeState
from lamor_flexbe_states.speech_output_state import SpeechOutputState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Sun Aug 30 2015
@author: Philipp Schillinger
'''
class TellRandomJokeSM(Behavior):
	'''
	Lets the robot tell a random joke.
	'''


	def __init__(self):
		super(TellRandomJokeSM, self).__init__()
		self.name = 'Tell Random Joke'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:30 y:365, x:130 y:365
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:30 y:40
			OperatableStateMachine.add('Pick_One_Joke',
										PickJokeState(joke_selection=PickJokeState.RANDOM),
										transitions={'done': 'Tell_The_Joke'},
										autonomy={'done': Autonomy.Off},
										remapping={'joke': 'joke'})

			# x:30 y:110
			OperatableStateMachine.add('Tell_The_Joke',
										SpeechOutputState(),
										transitions={'done': 'finished', 'failed': 'failed'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'text': 'joke'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
