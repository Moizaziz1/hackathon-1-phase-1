#!/usr/bin/env python3

"""
Vision-Language-Action (VLA) System Example

This example demonstrates a basic VLA system that integrates vision,
language understanding, and action execution. It processes natural
language commands and executes corresponding actions based on visual input.
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Image
from nav_msgs.msg import Odometry
import json
import math
import re


class VLASystem(Node):
    def __init__(self):
        super().__init__('vla_system')

        # Create subscribers
        self.voice_cmd_sub = self.create_subscription(
            String,
            '/voice_command',
            self.voice_command_callback,
            10
        )

        self.image_sub = self.create_subscription(
            Image,
            '/camera/image_raw',
            self.image_callback,
            10
        )

        self.odom_sub = self.create_subscription(
            Odometry,
            '/robot/odom',
            self.odom_callback,
            10
        )

        # Create publishers
        self.cmd_vel_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.feedback_pub = self.create_publisher(String, '/vla_feedback', 10)

        # Initialize OpenCV bridge if needed
        try:
            from cv_bridge import CvBridge
            self.bridge = CvBridge()
        except ImportError:
            self.bridge = None
            self.get_logger().warn('cv_bridge not available, image processing disabled')

        # State variables
        self.current_command = None
        self.detected_objects = []
        self.robot_x = 0.0
        self.robot_y = 0.0
        self.robot_theta = 0.0

        # Navigation parameters
        self.goal_tolerance = 0.2
        self.navigation_active = False

        # Command patterns for natural language understanding
        self.command_patterns = {
            'move_to': [
                r'go to (the )?(?P<target>.+)',
                r'move to (the )?(?P<target>.+)',
                r'navigate to (the )?(?P<target>.+)',
            ],
            'find': [
                r'find (the )?(?P<target>.+)',
                r'locate (the )?(?P<target>.+)',
            ]
        }

        # Color mappings for object identification
        self.color_mappings = {
            'red': ['red', 'red one', 'red object'],
            'blue': ['blue', 'blue one', 'blue object'],
            'green': ['green', 'green one', 'green object'],
            'yellow': ['yellow', 'yellow one', 'yellow object'],
        }

        self.get_logger().info('VLA System initialized')

    def voice_command_callback(self, msg):
        """Process natural language voice commands"""
        command_text = msg.data.lower()
        self.get_logger().info(f'Received voice command: {command_text}')

        # Parse the command using regex patterns
        parsed_command = self.parse_command(command_text)

        if parsed_command:
            self.current_command = parsed_command
            action = parsed_command['action']
            target = parsed_command['target']

            self.get_logger().info(f'Parsed command: {action} {target}')

            # Start navigation if it's a movement command
            if action in ['move_to', 'find']:
                self.start_navigation(parsed_command['properties'].get('color', 'unknown'))

                # Publish feedback
                feedback_msg = String()
                feedback_msg.data = f'Looking for {target}'
                self.feedback_pub.publish(feedback_msg)
        else:
            self.get_logger().info('Could not parse command')

    def image_callback(self, msg):
        """Process camera images for object detection"""
        if not self.bridge:
            return

        try:
            # Convert ROS image to OpenCV format
            cv_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")

            # In a real implementation, you would run object detection here
            # For this example, we'll simulate detection results
            simulated_objects = [
                {'color': 'red', 'position': {'x': 0.3, 'y': 0.4}, 'size': 15.0},
                {'color': 'blue', 'position': {'x': 0.7, 'y': 0.6}, 'size': 12.0},
                {'color': 'green', 'position': {'x': 0.5, 'y': 0.2}, 'size': 10.0}
            ]

            self.detected_objects = simulated_objects
            self.get_logger().info(f'Detected {len(simulated_objects)} objects')

        except Exception as e:
            self.get_logger().error(f'Error processing image: {e}')

    def odom_callback(self, msg):
        """Update robot position from odometry"""
        self.robot_x = msg.pose.pose.position.x
        self.robot_y = msg.pose.pose.position.y

        # Extract orientation (simplified)
        q = msg.pose.pose.orientation
        self.robot_theta = math.atan2(2.0 * (q.w * q.z + q.x * q.y),
                                     1.0 - 2.0 * (q.y * q.y + q.z * q.z))

    def parse_command(self, command_text):
        """Parse natural language command into structured format"""
        # Try to match command patterns
        for action, patterns in self.command_patterns.items():
            for pattern in patterns:
                match = re.search(pattern, command_text)
                if match:
                    target = match.group('target').strip()

                    # Identify object properties (color, etc.)
                    obj_properties = self.identify_object_properties(target)

                    # Create structured command
                    return {
                        'action': action,
                        'target': target,
                        'properties': obj_properties
                    }

        return None

    def identify_object_properties(self, target_text):
        """Identify object properties like color from text"""
        properties = {}

        # Check for colors in the target text
        for color, aliases in self.color_mappings.items():
            for alias in aliases:
                if alias in target_text:
                    properties['color'] = color
                    break
            if 'color' in properties:
                break

        return properties

    def start_navigation(self, target_color):
        """Start navigation to target object"""
        self.navigation_active = True
        self.target_color = target_color
        self.get_logger().info(f'Starting navigation to {target_color} object')

    def navigate_to_object(self, target_obj):
        """Navigate to the specified target object"""
        # Calculate relative position (0-1 in image coordinates)
        rel_x = target_obj['position']['x']
        rel_y = target_obj['position']['y']

        # Convert relative position to angular adjustment
        x_deviation = rel_x - 0.5  # Center of image is 0.5

        # Create twist command
        cmd = Twist()

        # If object is roughly centered, move forward
        if abs(x_deviation) < 0.1:
            cmd.linear.x = 0.3  # Move forward
            cmd.angular.z = 0.0
        else:
            # Rotate to center the object
            cmd.linear.x = 0.0
            cmd.angular.z = -x_deviation * 0.5  # Proportional control

        # If object is large enough, we're close enough
        if target_obj['size'] > 20:  # If object takes more than 20% of image
            cmd.linear.x = 0.0
            cmd.angular.z = 0.0
            self.get_logger().info(f'Reached target object')
            self.navigation_active = False

            # Publish completion feedback
            feedback_msg = String()
            feedback_msg.data = f'Reached target object'
            self.feedback_pub.publish(feedback_msg)

        self.cmd_vel_pub.publish(cmd)

    def search_for_object(self):
        """Search behavior when object is not detected"""
        # Implement a simple search pattern - rotate slowly
        cmd = Twist()
        cmd.angular.z = 0.2  # Slow rotation
        cmd.linear.x = 0.0
        self.cmd_vel_pub.publish(cmd)

    def find_target_object(self, target_color):
        """Find object of specified color from detected objects"""
        for obj in self.detected_objects:
            if obj.get('color', '').lower() == target_color.lower():
                return obj
        return None

    def control_loop(self):
        """Main control loop for the VLA system"""
        if not self.navigation_active or not self.current_command:
            return

        # Find target object
        target_obj = self.find_target_object(self.target_color)

        if target_obj:
            # Calculate navigation to target
            self.navigate_to_object(target_obj)
        else:
            # Object not detected, continue searching
            self.search_for_object()
            self.get_logger().info(f'Target {self.target_color} object not found, searching...')


def main(args=None):
    """Main function to initialize and run the ROS 2 node"""
    rclpy.init(args=args)

    vla_system = VLASystem()

    try:
        rclpy.spin(vla_system)
    except KeyboardInterrupt:
        pass
    finally:
        # Stop the robot before shutting down
        cmd = Twist()
        cmd.linear.x = 0.0
        cmd.angular.z = 0.0
        vla_system.cmd_vel_pub.publish(cmd)

        vla_system.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()