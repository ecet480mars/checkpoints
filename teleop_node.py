#!/usr/bin/env python

# Start of the script
import rospy
from geometry_msgs.msg import Twist
import sys, select, termios, tty

# Key mappings
key_mapping = {
    'w': [1, 0],
    'a': [0, 1],
    's': [-1, 0],
    'd': [0, -1],
}

# Speed adjustment mappings
speed_mapping = {
    'r': [1, 0],
    'f': [-1, 0],
    'q': [0, 1],
    'e': [0, -1],
}

# Function to get the key pressed
def getKey():
    tty.setraw(sys.stdin.fileno())
    select.select([sys.stdin], [], [], 0)
    key = sys.stdin.read(1)
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

if __name__ == "__main__":
    # Save the current terminal settings
    settings = termios.tcgetattr(sys.stdin)

    # Initialize a ROS node called 'wasd_controller'
    rospy.init_node('wasd_controller')

    # Create a publisher for the 'cmd_vel' topic with message type Twist
    pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)

    # Set initial linear and angular speeds
    linear_speed = 0.5
    angular_speed = 1.0

    # Set the increment value for adjusting speeds
    speed_increment = 0.1

    try:
        while not rospy.is_shutdown():
            key = getKey()

            if key in key_mapping:
                linear, angular = key_mapping[key]
                twist = Twist()
                twist.linear.x = linear_speed * linear
                twist.angular.z = angular_speed * angular
                pub.publish(twist)

            elif key in speed_mapping:
                delta_linear, delta_angular = speed_mapping[key]
                linear_speed += speed_increment * delta_linear
                angular_speed += speed_increment * delta_angular
                rospy.loginfo("Updated Speeds -> Linear: %.2f, Angular: %.2f", linear_speed, angular_speed)

            elif key == 'x':
                rospy.loginfo("Exiting teleop...")
                break

            else:
                continue

    except rospy.ROSInterruptException:
        pass

    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
