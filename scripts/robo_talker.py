#!/usr/bin/env python
# Software License Agreement (BSD License)
#
# Copyright (c) 2008, Willow Garage, Inc.
# All rights reserved.
import rospy
from std_msgs.msg import String

global subscr_wr
global subscr_db
global subscr_wc
global status_code
def callback_wr(data): 
    msg = data.data
    print(msg)
    global MSG
    MSG = msg
    subscr_wr.unregister()

def callback_db(data):
    msg = data.data
    print(msg)
    MSG = msg
    subscr_db.unregister()

def callback_wc(data):
    msg = data.data
    print(msg)
    MSG = msg
    subscr_wc.unregister()

subscr_wr = rospy.Subscriber('result_wr',String,callback_wr)
subscr_db = rospy.Subscriber('result_db',String,callback_db)
subscr_wc = rospy.Subscriber('result_wc',String,callback_wc)
MSG = None

def talker_wr(message):
    pub = rospy.Publisher('chatter_wr', String, queue_size=1)
    rospy.init_node('talker', anonymous=True)
    if not rospy.is_shutdown():
        pub.publish(message)
        subscr_wr = rospy.Subscriber('result_wr',String,callback_wr)
        rospy.spin()

def talker_db(message):
    pub = rospy.Publisher('chatter_db', String, queue_size=15)
    rospy.init_node('talker', anonymous=True)
    if not rospy.is_shutdown():
        pub.publish(message)
        subscr_db = rospy.Subscriber('result_db',String,callback_db)

def talker_wc(message):
    pub = rospy.Publisher('chatter_wc', String, queue_size=15)
    rospy.init_node('talker', anonymous=True)
    if not rospy.is_shutdown():
        pub.publish(message)
        subscr_wc = rospy.Subscriber('result_wc',String,callback_wc)

def talker(message,path):
    if message == 1:
        talker_wr(path)
    if message == 2:
        talker_db(path)
    if message == 3:
        talker_wc(path)
    return MSG

if __name__ == '__main__':
    try:
        status_code = 1
        talker(status_code,"/static/audio/hts0000f2e1@ch09280e6320d4477500.wav")
    except rospy.ROSInterruptException:
        pass
