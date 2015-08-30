#ifndef STALK_AT_POSE_H
#define STALK_AT_POSE_H

#include <ros/ros.h>
#include <ros/time.h>
#include <geometry_msgs/PoseArray.h>
#include <geometry_msgs/Pose.h>
#include <geometry_msgs/PoseStamped.h>
#include <sensor_msgs/JointState.h>
#include <tf/transform_listener.h>
#include <actionlib/server/simple_action_server.h>
#include <actionlib/client/simple_action_client.h>
#include <move_base_msgs/MoveBaseAction.h>
#include <stalk/StalkPoseAction.h>

#include <limits>

#include <boost/thread.hpp>

class StalkPose
{
public:
    StalkPose(std::string name);
    ~StalkPose();
    void callback(const geometry_msgs::PoseStamped::ConstPtr &msg);
    void goalCallback(ros::NodeHandle &n);
    void preemptCallback();
    void MoveBaseDone(const actionlib::SimpleClientGoalState& state,
                      const boost::shared_ptr<move_base_msgs::MoveBaseResult>& result);

private:
    void init();
    void inline feedback(geometry_msgs::Pose pose);
    void inline checkTime();
    void transform();
    void setPose(const geometry_msgs::PoseStamped::ConstPtr &msg);
    const geometry_msgs::PoseStamped::ConstPtr getPose();
    void resetHead();

    ros::Publisher head_pose_pub;
    ros::Subscriber pose_array_sub;
    tf::TransformListener* listener;
    actionlib::SimpleActionServer<stalk::StalkPoseAction> *as_;
    actionlib::SimpleActionClient<move_base_msgs::MoveBaseAction> *mbc_;
    boost::shared_ptr<const stalk::StalkPoseGoal> goal_;
    stalk::StalkPoseFeedback feedback_;
    stalk::StalkPoseResult result_;
    std::string action_name_;
    std::string target_frame;
    double end_time;
    int timeToBlink;
    int timeToUnBlink;
    geometry_msgs::PoseStamped::ConstPtr pose;
    boost::mutex mutex;
    boost::thread transform_thread;
};

#endif // STALK_AT_POSE_H
