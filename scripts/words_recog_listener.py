#!/usr/bin/env python
# Software License Agreement (BSD License)
#
# Copyright (c) 2008, Willow Garage, Inc.
# All rights reserved.
import rospy
from std_msgs.msg import String
from wordsRecog import recog

def callback_wr(data):
    path = data.data
    result_wr = recog(path)
    pub = rospy.Publisher('result_wr', String, queue_size=15)
    pub.publish(result_wr)
    print(result_wr)

def listener_wr():
    rospy.init_node('listener_wr',anonymous=True)
    rospy.Subscriber('chatter_wr',String,callback_wr)
    rospy.spin()

if __name__ == '__main__':
    listener_wr()