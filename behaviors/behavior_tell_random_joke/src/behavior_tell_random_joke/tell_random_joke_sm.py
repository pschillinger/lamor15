#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

import roslib; roslib.load_manifest('behavior_tell_random_joke')
from flexbe_core import Behavior, Autonomy, OperatableStateMachine, Logger
from lamor_flexbe_states.detect_person_state import DetectPersonState
from lamor_flexbe_states.move_camera_state import MoveCameraState
from lamor_flexbe_states.approach_person_state import ApproachPersonState
from lamor_flexbe_states.take_picture_state import TakePictureState
from lamor_flexbe_states.detect_face_state import DetectFaceState
from lamor_flexbe_states.speech_output_state import SpeechOutputState
from lamor_flexbe_states.pick_joke_state import PickJokeState
from flexbe_states.wait_state import WaitState
from lamor_flexbe_states.store_picture_state import StorePictureState
from lamor_flexbe_states.show_picture_webinterface_state import ShowPictureWebinterfaceState
from lamor_flexbe_states.tweet_picture_state import TweetPictureState
from flexbe_states.calculation_state import CalculationState
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
		wait_timeout = 30 # seconds
		max_approach_index = 8
		tweet_template = '#LAMoR15 #ECMR15 I just told a joke: %s'
		# x:705 y:482, x:130 y:365
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
		_state_machine.userdata.approach_index = 0
		_state_machine.userdata.text_too_far = "Sorry, I am unable to come closer! But I can tell you a joke!"
		_state_machine.userdata.text_come_around = "I just took a picture of you. You can come around and take a look."
		_state_machine.userdata.text_tweeted = "I tweeted the picture!"
		_state_machine.userdata.cam_pan = 0 # deg right
		_state_machine.userdata.cam_tilt = 20 # deg down

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]

		# x:121 y:471
		_sm_take_a_picture_0 = OperatableStateMachine(outcomes=['finished'], input_keys=['joke', 'text_come_around', 'text_tweeted'])

		with _sm_take_a_picture_0:
			# x:91 y:28
			OperatableStateMachine.add('Wait_For_Laughing',
										WaitState(wait_time=1),
										transitions={'done': 'Take_Picture'},
										autonomy={'done': Autonomy.Off})

			# x:98 y:228
			OperatableStateMachine.add('Store_Picture',
										StorePictureState(),
										transitions={'done': 'Say_Come_Around'},
										autonomy={'done': Autonomy.Off},
										remapping={'Image': 'Image', 'filename': 'image_name'})

			# x:99 y:128
			OperatableStateMachine.add('Take_Picture',
										TakePictureState(),
										transitions={'done': 'Store_Picture'},
										autonomy={'done': Autonomy.Off},
										remapping={'Image': 'Image'})

			# x:68 y:328
			OperatableStateMachine.add('Show_Picture',
										ShowPictureWebinterfaceState(),
										transitions={'tweet': 'Append_Text', 'forget': 'finished'},
										autonomy={'tweet': Autonomy.Off, 'forget': Autonomy.Off},
										remapping={'image_name': 'image_name'})

			# x:324 y:428
			OperatableStateMachine.add('Tweet_Picture',
										TweetPictureState(),
										transitions={'picture_tweeted': 'Tell_Tweeted', 'tweeting_failed': 'finished', 'command_error': 'finished'},
										autonomy={'picture_tweeted': Autonomy.Off, 'tweeting_failed': Autonomy.Off, 'command_error': Autonomy.Off},
										remapping={'picture_path': 'image_name', 'tweet_text': 'tweet_text'})

			# x:360 y:289
			OperatableStateMachine.add('Append_Text',
										CalculationState(calculation=lambda x: tweet_template % x),
										transitions={'done': 'Tweet_Picture'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'joke', 'output_value': 'tweet_text'})

			# x:251 y:182
			OperatableStateMachine.add('Say_Come_Around',
										SpeechOutputState(),
										transitions={'done': 'Show_Picture', 'failed': 'finished'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'text': 'text_come_around'})

			# x:246 y:522
			OperatableStateMachine.add('Tell_Tweeted',
										SpeechOutputState(),
										transitions={'done': 'finished', 'failed': 'finished'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'text': 'text_tweeted'})


		# x:392 y:544, x:922 y:602, x:128 y:248
		_sm_approach_person_1 = OperatableStateMachine(outcomes=['finished', 'unable_to_approach', 'no_person'], input_keys=['approach_index', 'pan', 'tilt'])

		with _sm_approach_person_1:
			# x:92 y:78
			OperatableStateMachine.add('Check_For_Person',
										DetectPersonState(wait_timeout=wait_timeout),
										transitions={'detected': 'Take_Picture', 'not_detected': 'no_person'},
										autonomy={'detected': Autonomy.Off, 'not_detected': Autonomy.Off},
										remapping={'person_pose': 'person_pose'})

			# x:563 y:394
			OperatableStateMachine.add('Adjust_Camera',
										MoveCameraState(),
										transitions={'done': 'finished', 'failed': 'unable_to_approach'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'pan': 'pan', 'tilt': 'tilt'})

			# x:598 y:66
			OperatableStateMachine.add('Approach_Person',
										ApproachPersonState(),
										transitions={'goal_reached': 'Adjust_Camera', 'goal_failed': 'Adjust_Camera', 'command_error': 'Adjust_Camera'},
										autonomy={'goal_reached': Autonomy.Off, 'goal_failed': Autonomy.Off, 'command_error': Autonomy.Off},
										remapping={'person_pose': 'person_pose'})

			# x:363 y:39
			OperatableStateMachine.add('Take_Picture',
										TakePictureState(),
										transitions={'done': 'Check_For_Faces'},
										autonomy={'done': Autonomy.Off},
										remapping={'Image': 'Image'})

			# x:381 y:158
			OperatableStateMachine.add('Check_For_Faces',
										DetectFaceState(),
										transitions={'face_is_detected': 'Approach_Person', 'face_is_not_detected': 'Check_For_Person'},
										autonomy={'face_is_detected': Autonomy.Off, 'face_is_not_detected': Autonomy.Off},
										remapping={'Image': 'Image'})



		with _state_machine:
			# x:82 y:72
			OperatableStateMachine.add('Approach_Person',
										_sm_approach_person_1,
										transitions={'finished': 'Pick_One_Joke', 'unable_to_approach': 'Tell_Too_Far', 'no_person': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'unable_to_approach': Autonomy.Inherit, 'no_person': Autonomy.Inherit},
										remapping={'approach_index': 'approach_index', 'pan': 'cam_pan', 'tilt': 'cam_tilt'})

			# x:444 y:228
			OperatableStateMachine.add('Tell_The_Joke',
										SpeechOutputState(),
										transitions={'done': 'Take_A_Picture', 'failed': 'failed'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.High},
										remapping={'text': 'joke'})

			# x:244 y:178
			OperatableStateMachine.add('Tell_Too_Far',
										SpeechOutputState(),
										transitions={'done': 'Pick_One_Joke', 'failed': 'failed'},
										autonomy={'done': Autonomy.Low, 'failed': Autonomy.High},
										remapping={'text': 'text_too_far'})

			# x:451 y:78
			OperatableStateMachine.add('Pick_One_Joke',
										PickJokeState(joke_selection=PickJokeState.RANDOM),
										transitions={'done': 'Tell_The_Joke'},
										autonomy={'done': Autonomy.Off},
										remapping={'joke': 'joke'})

			# x:704 y:119
			OperatableStateMachine.add('Take_A_Picture',
										_sm_take_a_picture_0,
										transitions={'finished': 'finished'},
										autonomy={'finished': Autonomy.Inherit},
										remapping={'joke': 'joke', 'text_come_around': 'text_come_around', 'text_tweeted': 'text_tweeted'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
