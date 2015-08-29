#!/bin/bash

SESSION=$USER

tmux -2 new-session -d -s $SESSION
# Setup a window for tailing log files
tmux new-window -t $SESSION:0 -n 'roscore'
tmux new-window -t $SESSION:1 -n 'core'
tmux new-window -t $SESSION:2 -n 'simulation'
tmux new-window -t $SESSION:3 -n 'navigation'


tmux select-window -t $SESSION:0
tmux split-window -v
tmux select-pane -t 0
tmux send-keys "roscore" C-m
tmux resize-pane -U 30
tmux select-pane -t 1
tmux send-keys "htop" C-m

tmux select-window -t $SESSION:1
tmux send-keys "DISPLAY=:0 roslaunch mongodb_store mongodb_store.launch db_path:=$HOME/mongodb_lamor"

tmux select-window -t $SESSION:2
tmux send-keys "DISPLAY=:0 roslaunch strands_morse uol_bl_morse.launch env:=uol_bl_fast"

tmux select-window -t $SESSION:3
tmux send-keys "DISPLAY=:0 roslaunch lamor_bringup lamor_sim_navigation.launch dataset:=bl_sim map:=\$(rospack find strands_morse)/uol/maps/uol_bl.yaml"


# Set default window
tmux select-window -t $SESSION:0

# Attach to session
tmux -2 attach-session -t $SESSION

tmux setw -g mode-mouse off
