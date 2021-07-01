#!/usr/bin/env python
import rospy
import sys
import numpy as np
import quaternion
sys.path.append("triad_openvr")
from geometry_msgs.msg import Pose

import triad_openvr as vr
import time
import sys
import tf
import pybullet as pb
pi = 3.141592
def publisher():
    pub = rospy.Publisher('pose', Pose, queue_size=1)
    rospy.init_node('pose_publisher', anonymous=True)
    rate = rospy.Rate(90) # Hz


    v = vr.triad_openvr()
    v.print_discovered_objects()

    if len(sys.argv) == 1:
        interval = 1/250
    elif len(sys.argv) == 2:
        interval = 1/float(sys.argv[1])
    else:
        print("Invalid number of arguments")
        interval = False

    basepose = pb.getQuaternionFromEuler([0,0,0])	
    sumquat = pb.getQuaternionFromEuler([0,0,pi])
    sumquat = np.quaternion(sumquat[0],sumquat[1],sumquat[2],sumquat[3])
    sumquat_R = quaternion.as_rotation_matrix(sumquat)
    while not rospy.is_shutdown():
	try:
		p = Pose()
		br = tf.TransformBroadcaster()    
		pose_data = v.devices["tracker_1"].get_pose_quaternion()
		pose_data2 = v.devices["tracker_1"].get_pose_euler()
		p.position.x = pose_data[0]
		p.position.y = pose_data[1]
		p.position.z = pose_data[2]
		# Make sure the quaternion is valid and normalized
		p.orientation.x = pose_data[3]
		p.orientation.y = pose_data[4]
		p.orientation.z = pose_data[5]
		p.orientation.w = pose_data[6]
		pub.publish(p)
		br.sendTransform((0,0,1.6),basepose,rospy.Time.now(),"vive_base","world")
		posequat = quaternion.as_quat_array([pose_data[3],pose_data[4],pose_data[5],pose_data[6]])
		posequat_R = quaternion.as_rotation_matrix(posequat)
		R =np.matmul(sumquat_R,posequat_R)
		resultquat = quaternion.from_rotation_matrix(R, nonorthogonal=True)
		resultquat = quaternion.as_float_array(resultquat)

		#print(resultquat)
		br.sendTransform((-pose_data[2], -pose_data[0], pose_data[1]),
		     (resultquat[0],resultquat[2],resultquat[1],resultquat[3]),
		     rospy.Time.now(),
		     "tracker",
		     "vive_base")
		rate.sleep()
	except Exception as inst:
		print(inst)
		pass

if __name__ == '__main__':
    try:
        publisher()
    except rospy:
        pass
