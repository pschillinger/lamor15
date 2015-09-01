#!/bin/bash

SESSION=$USER + "_red"

tmux -2 new-session -d -s $SESSION
# Setup a window for tailing log files
tmux new-window -t $SESSION:0 -n 'stalking'
tmux new-window -t $SESSION:1 -n 'flexbe'
tmux new-window -t $SESSION:2 -n 'fbe action'
tmux new-window -t $SESSION:3 -n 'routine'


tmux select-window -t $SESSION:0
tmux send-keys "rosrun stalking stalk_pose"

tmux select-window -t $SESSION:1
tmux send-keys "roslaunch flexbe_onboard behavior_onboard.launch"

tmux select-window -t $SESSION:2
tmux send-keys "rosrun flexbe_widget be_action_server"

tmux select-window -t $SESSION:3
tmux send-keys "rosrun lamor_bringup linda_wander_routine.py"


# Set default window
tmux select-window -t $SESSION:0

# Attach to session
tmux -2 attach-session -t $SESSION

tmux setw -g mode-mouse off