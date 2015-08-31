# Stalking behavior 

Created by hacking the strands gaze_at_pose behavior. The `goal` message is composed of the behavior `runtime` (how long to gaze, 0 means forever), the `topic_name` of the topic where the tracker publishes human pose data (use `/human/poses` for simulation, `/upper_body_detector/closest_bounding_box_centre` for the real robot) and a `target` `PoseStamped` which specifies the current position of the tracked person. The robot stops 0.7 meters away from the specified target to give the person some room to breathe :)

To test the behavior in simulation, use

```
rosrun actionlib axclient.py /stalk_pose
```

with the following goal message:

```
runtime_sec: 0
topic_name: '/human/poses'
target: 
  header: 
    seq: 0
    stamp: 
      secs: 0
      nsecs: 0
    frame_id: '/map'
  pose: 
    position: 
      x: -1.0
      y: -5.0
      z: 0.0
    orientation: 
      x: 0.0
      y: 0.0
      z: 0.0
      w: 1.0
```

For further details consult the docs of the strands gazing package.
