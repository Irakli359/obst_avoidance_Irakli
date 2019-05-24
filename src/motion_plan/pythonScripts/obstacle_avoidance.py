#! /usr/bin/env python

import rospy

from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
pub = None
global_linear_x = 0
global_angular_z = 0
state_description = ''
class Server:
    def __init__(self):
        self.linear_x  = 0
        self.angular_z= 0
	self.msg1 = rospy.Subscriber('/key_vel', Twist, self.clbk_keyboard)
        self.msg2 = rospy.Subscriber('/mybot/laser/scan', LaserScan, self.clbk_laser)
    def clbk_keyboard(self,msg1):
    	self.linear_x = msg1.linear.x
    	self.angular_z = msg1.angular.z
    def clbk_laser(self,msg2):
    	regions = {
        	'right':  min(min(msg2.ranges[0:143]), 100),
        	'fright': min(min(msg2.ranges[144:287]), 100),
        	'front':  min(min(msg2.ranges[288:431]), 100),
        	'fleft':  min(min(msg2.ranges[432:575]), 100),
        	'left':   min(min(msg2.ranges[576:719]), 100),
    	}
    	self.take_action(regions)
    def take_action(self,regions):
	global state_description
    	linear_x = 0 
    	angular_z = 0
    	msg = Twist()
    	d = 1
	average_rotation_speed = 0.25
    	if regions['front'] > d and regions['fleft'] > d and regions['fright'] > d:

        	state_description = 'case 1 - nothing in front'
        	linear_x = self.linear_x
        	angular_z = self.angular_z
    	elif regions['front'] < d and regions['fleft'] > d and regions['fright'] > d :
        	state_description = 'case 2 - front'
        	linear_x= self.linear_x/2
        	if(self.angular_z > 0 and self.angular_z <0.3):
			angular_z = self.angular_z +0.15
		else:
			angular_z = average_rotation_speed
        	self.angular_z= 0
    	elif regions['front'] > d and regions['fleft'] > d and regions['fright'] < d :
		state_description = 'case 3 - fright'
        	linear_x= self.linear_x/2
        	if(self.angular_z > 0 and self.angular_z <0.3):
			angular_z = self.angular_z +0.15
		else:
			angular_z = average_rotation_speed
        	self.angular_z= 0
    	elif regions['front'] > d  and regions['fleft'] < d and regions['fright'] > d :
        	state_description = 'case 4 - fleft'
        	linear_x= self.linear_x/2
        	if(self.angular_z > -0.3 and self.angular_z <0):
			angular_z = self.angular_z -0.15
		else:
			angular_z = average_rotation_speed*(-1)
        	self.angular_z= 0
	
    	elif regions['front'] < d  and regions['fleft'] > d and regions['fright'] < d :
        	state_description = 'case 5 - front and fright'
        	linear_x= self.linear_x/2
        	if(self.angular_z > 0 and self.angular_z <0.3):
			angular_z = self.angular_z +0.15
		else:
			angular_z = average_rotation_speed 
        	self.angular_z= 0
    	elif regions['front'] < d and regions['fleft'] < d and regions['fright'] > d :
        	state_description = 'case 6 - front and fleft'
        	linear_x= self.linear_x/2
        	if(self.angular_z > -0.3 and self.angular_z <0):
			angular_z = self.angular_z -0.15
		else:
			angular_z = average_rotation_speed*(-1)
        	self.angular_z= 0
	
    	elif regions['front'] < d  and regions['fleft'] < d and regions['fright'] < d :
        	state_description = 'case 7 - front and fleft and fright'
        	linear_x= self.linear_x/2
        	angular_z = average_rotation_speed + 0.12
        	self.angular_z= 0
    	elif regions['front'] > d and regions['fleft'] < d and regions['fright'] < d :
        	state_description = 'case 8 - fleft and fright'
        	linear_x= self.linear_x/2
        	self.angular_z= 0
    	else:
        	state_description = 'unknown case'
        	rospy.loginfo(regions)
        rospy.loginfo(state_description)
    	msg.linear.x = linear_x
    	msg.angular.z = angular_z
    	pub.publish(msg)

def main():
    global pub
    rospy.init_node('Obstacle_Avoidance')
    server = Server()
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)

    
    rospy.spin()

if __name__ == '__main__':
    main()

