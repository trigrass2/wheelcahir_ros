#!/usr/bin/env python
# coding: UTF-8

import rospy
import math
from geometry_msgs.msg import PoseWithCovarianceStamped
from geometry_msgs.msg import Pose
from geometry_msgs.msg import PoseStamped
from move_base_msgs.msg import MoveBaseActionGoal


APPRORCH_THRESHOLD = 0.5  # 何mまで近づいたら次の点を指示するか


class playRecordedWaypoint:

    recorded_waypoints = []
    index = 0

    def __init__(self):
        rospy.init_node('play_waypoint', anonymous=True)
        self.pub = rospy.Publisher('/move_base_simple/goal', PoseStamped, queue_size=10)
        self.get_waypoints_from_txt()

    def calc_distance_between_poses(self,pose1,pose2):
        return math.sqrt( abs( (pose1.position.x - pose2.position.x)*(pose1.position.x - pose2.position.x) + (pose1.position.y - pose2.position.y)*(pose1.position.y - pose2.position.y) ) )

    def callback(self,data):

        pose_info = data.pose.pose
    
        if len(self.recorded_waypoints) - 1 > self.index:
            if self.calc_distance_between_poses( self.recorded_waypoints[self.index] , pose_info ) < APPRORCH_THRESHOLD:
                self.index += 1
                pub_pose = MoveBaseActionGoal()
                pub_pose.header = data.header
                pub_pose.goal.target_pose.header = data.header
                pub_pose.goal.target_pose.pose   = self.recorded_waypoints[self.index]
                self.pub.publish(pub_pose)
                print pub_pose


    def get_waypoints_from_txt(self):

        f=open('waypoint.txt','r')

        for i in f.readlines():
        
            #print i
            i=i.strip()         #末尾の改行を除去
            i=i.split("\t")     #空白(tab)で文字列を区切り、リストを作成

            pose_info = Pose()

            pose_info.position.x    = float(i[0])
            pose_info.position.y    = float(i[1])
            pose_info.position.z    = float(i[2])
            pose_info.orientation.x = float(i[3])
            pose_info.orientation.x = float(i[4])
            pose_info.orientation.x = float(i[5])
            pose_info.orientation.x = float(i[6])

            self.recorded_waypoints.append(pose_info)

        f.close()
        #print self.recorded_waypoints

    def listener(self):
        odom_topic = rospy.get_param('odom_topic',"/amcl_pose")
        rospy.Subscriber(odom_topic,PoseWithCovarianceStamped, self.callback)
        pub_pose = MoveBaseActionGoal()
        pub_pose.goal.target_pose.pose   = self.recorded_waypoints[self.index]
        self.pub.publish(pub_pose)
        rospy.spin()
    

        


if __name__ == '__main__':
    processer = playRecordedWaypoint()
    processer.listener()