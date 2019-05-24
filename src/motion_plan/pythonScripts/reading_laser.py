#! /usr/bin/env python

import rospy

from sensor_msgs.msg import LaserScan

def clbk_laser(msg):
    # 720 / 5 = 144
    regions = [
        min(min(msg.ranges[0:143]), 100),
        min(min(msg.ranges[144:287]), 100),
        min(min(msg.ranges[288:431]), 100),
        min(min(msg.ranges[432:575]), 100),
        min(min(msg.ranges[576:713]), 100),
    ]
    rospy.loginfo(regions)

def main():
    rospy.init_node('reading_laser')
    
    sub = rospy.Subscriber('/mybot/laser/scan', LaserScan, clbk_laser)
    
    rospy.spin()

if __name__ == '__main__':
    main()

