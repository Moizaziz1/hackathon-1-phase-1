---
sidebar_label: 'Lab 1: Basic VLA System'
sidebar_position: 1
---

# Lab 1: Basic Vision-Language-Action System

In this lab, you'll implement a basic Vision-Language-Action (VLA) system that can understand simple natural language commands and execute corresponding actions based on visual input. You'll create a system that can detect colored objects and move toward them based on voice commands.

## Learning Objectives

After completing this lab, you will be able to:
- Integrate vision, language, and action components in a unified system
- Process natural language commands to identify target objects
- Execute navigation actions based on visual and linguistic inputs
- Create a basic VLA pipeline using ROS 2

## Prerequisites

Before starting this lab, ensure you have:
- Completed the ROS 2 fundamentals, simulation, and perception modules
- Basic understanding of natural language processing concepts
- Access to a simulated robot with camera and navigation capabilities
- OpenCV and basic NLP libraries installed

## Step 1: Create the VLA Package

First, create a new ROS 2 package for the VLA system:

```bash
cd ~/ros2_labs/src
ros2 pkg create --build-type ament_python vla_tutorial
cd vla_tutorial
mkdir -p vla_tutorial
```

## Step 2: Create the Command Parser Node

Create a simple command parser that converts natural language to actionable commands at `vla_tutorial/command_parser.py`:

```python
#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import Point
import re


class CommandParser(Node):
    def __init__(self):
        super().__init__('command_parser')

        # Create subscriber for voice commands
        self.voice_sub = self.create_subscription(
            String,
            '/voice_command',
            self.voice_callback,
            10
        )

        # Create publisher for parsed commands
        self.command_pub = self.create_publisher(String, '/parsed_command', 10)

        # Define command patterns
        self.command_patterns = {
            'move_to': [
                r'go to (the )?(?P<target>.+)',
                r'move to (the )?(?P<target>.+)',
                r'navigate to (the )?(?P<target>.+)',
                r'go get (the )?(?P<target>.+)',
            ],
            'find': [
                r'find (the )?(?P<target>.+)',
                r'locate (the )?(?P<target>.+)',
                r'look for (the )?(?P<target>.+)',
            ],
            'grasp': [
                r'pick up (the )?(?P<target>.+)',
                r'grasp (the )?(?P<target>.+)',
                r'get (the )?(?P<target>.+)',
            ]
        }

        # Define color mappings
        self.color_mappings = {
            'red': ['red', 'red one', 'red object'],
            'blue': ['blue', 'blue one', 'blue object'],
            'green': ['green', 'green one', 'green object'],
            'yellow': ['yellow', 'yellow one', 'yellow object'],
            'white': ['white', 'white one', 'white object'],
            'black': ['black', 'black one', 'black object'],
        }

        self.get_logger().info('Command Parser initialized')

    def voice_callback(self, msg):
        command_text = msg.data.lower()
        self.get_logger().info(f'Received command: {command_text}')

        # Parse the command
        parsed_command = self.parse_command(command_text)

        if parsed_command:
            command_msg = String()
            command_msg.data = parsed_command
            self.command_pub.publish(command_msg)
            self.get_logger().info(f'Parsed command: {parsed_command}')
        else:
            self.get_logger().info('Could not parse command')

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
                    structured_cmd = {
                        'action': action,
                        'target': target,
                        'properties': obj_properties
                    }

                    return f"{action}:{target}:{obj_properties.get('color', 'unknown')}"

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


def main(args=None):
    rclpy.init(args=args)

    parser = CommandParser()

    try:
        rclpy.spin(parser)
    except KeyboardInterrupt:
        pass
    finally:
        parser.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
```

## Step 3: Create the VLA Coordinator Node

Create the main VLA coordinator that integrates vision, language, and action at `vla_tutorial/vla_coordinator.py`:

```python
#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import Twist, Point
from nav_msgs.msg import Odometry
import json
import math


class VLA_Coordinator(Node):
    def __init__(self):
        super().__init__('vla_coordinator')

        # Create subscribers
        self.parsed_cmd_sub = self.create_subscription(
            String,
            '/parsed_command',
            self.parsed_cmd_callback,
            10
        )

        self.detected_objects_sub = self.create_subscription(
            String,
            '/detected_objects',  # From perception tutorial
            self.detected_objects_callback,
            10
        )

        self.odom_sub = self.create_subscription(
            Odometry,
            '/simple_robot/odom',  # From simulation
            self.odom_callback,
            10
        )

        # Create publishers
        self.cmd_vel_pub = self.create_publisher(Twist, '/simple_robot/cmd_vel', 10)
        self.feedback_pub = self.create_publisher(String, '/vla_feedback', 10)

        # State variables
        self.current_command = None
        self.detected_objects = []
        self.current_x = 0.0
        self.current_y = 0.0
        self.current_theta = 0.0

        # Navigation parameters
        self.goal_tolerance = 0.2
        self.rotation_threshold = 0.1
        self.navigation_active = False

        # Timer for control loop
        self.timer = self.create_timer(0.1, self.control_loop)

        self.get_logger().info('VLA Coordinator initialized')

    def parsed_cmd_callback(self, msg):
        """Handle parsed commands from command parser"""
        try:
            command_parts = msg.data.split(':')
            if len(command_parts) >= 3:
                action = command_parts[0]
                target = command_parts[1]
                color = command_parts[2]

                self.get_logger().info(f'Received command: {action} {color} {target}')

                # Store the command for processing
                self.current_command = {
                    'action': action,
                    'target': target,
                    'color': color
                }

                # Start navigation if it's a move command
                if action in ['move_to', 'go_to', 'navigate_to', 'find']:
                    self.start_navigation(color)
                else:
                    self.get_logger().info(f'Action {action} not yet implemented')

        except Exception as e:
            self.get_logger().error(f'Error parsing command: {e}')

    def detected_objects_callback(self, msg):
        """Handle detected objects from perception system"""
        try:
            self.detected_objects = json.loads(msg.data)
        except json.JSONDecodeError:
            self.get_logger().error('Could not parse detected objects JSON')

    def odom_callback(self, msg):
        """Handle robot odometry"""
        self.current_x = msg.pose.pose.position.x
        self.current_y = msg.pose.pose.position.y

        # Extract orientation (simplified)
        q = msg.pose.pose.orientation
        self.current_theta = math.atan2(2.0 * (q.w * q.z + q.x * q.y),
                                       1.0 - 2.0 * (q.y * q.y + q.z * q.z))

    def start_navigation(self, target_color):
        """Start navigation to target object"""
        self.navigation_active = True
        self.target_color = target_color
        self.get_logger().info(f'Starting navigation to {target_color} object')

        # Publish feedback
        feedback_msg = String()
        feedback_msg.data = f'Looking for {target_color} object'
        self.feedback_pub.publish(feedback_msg)

    def control_loop(self):
        """Main control loop for navigation"""
        if not self.navigation_active or not self.current_command:
            return

        # Find target object
        target_obj = self.find_target_object(self.current_command['color'])

        if target_obj:
            # Calculate navigation to target
            self.navigate_to_object(target_obj)
        else:
            # Object not detected, continue searching
            self.search_for_object()
            self.get_logger().info(f'Object {self.current_command["color"]} not found, searching...')

    def find_target_object(self, target_color):
        """Find object of specified color from detected objects"""
        for obj in self.detected_objects:
            if obj.get('color', '').lower() == target_color.lower():
                return obj
        return None

    def navigate_to_object(self, target_obj):
        """Navigate to the specified target object"""
        # Calculate relative position (0-1 in image coordinates)
        rel_x = target_obj['position']['x']
        rel_y = target_obj['position']['y']

        # Convert relative position to angular adjustment
        # Center of image is (0.5, 0.5), so calculate deviation
        x_deviation = rel_x - 0.5
        y_deviation = rel_y - 0.5

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
            self.get_logger().info(f'Reached {self.current_command["color"]} object')
            self.navigation_active = False

            # Publish completion feedback
            feedback_msg = String()
            feedback_msg.data = f'Reached {self.current_command["color"]} object'
            self.feedback_pub.publish(feedback_msg)

        self.cmd_vel_pub.publish(cmd)

    def search_for_object(self):
        """Search behavior when object is not detected"""
        # Implement a simple search pattern - rotate slowly
        cmd = Twist()
        cmd.angular.z = 0.2  # Slow rotation
        cmd.linear.x = 0.0
        self.cmd_vel_pub.publish(cmd)

        # Publish searching feedback
        feedback_msg = String()
        feedback_msg.data = f'Searching for {self.current_command["color"]} object'
        self.feedback_pub.publish(feedback_msg)


def main(args=None):
    rclpy.init(args=args)

    coordinator = VLA_Coordinator()

    try:
        rclpy.spin(coordinator)
    except KeyboardInterrupt:
        pass
    finally:
        # Stop the robot before shutting down
        cmd = Twist()
        cmd.linear.x = 0.0
        cmd.angular.z = 0.0
        coordinator.cmd_vel_pub.publish(cmd)

        coordinator.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
```

## Step 4: Create a Simple Voice Command Simulator

Create a simple node to simulate voice commands at `vla_tutorial/voice_simulator.py`:

```python
#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import time


class VoiceSimulator(Node):
    def __init__(self):
        super().__init__('voice_simulator')

        # Create publisher for voice commands
        self.voice_pub = self.create_publisher(String, '/voice_command', 10)

        # Create timer to send commands periodically
        self.timer = self.create_timer(5.0, self.send_command)

        # Command queue
        self.commands = [
            "go to the red object",
            "move to the blue object",
            "find the green object",
        ]
        self.command_index = 0

        self.get_logger().info('Voice Simulator initialized')

    def send_command(self):
        """Send a command from the queue"""
        if self.commands:
            command = self.commands[self.command_index % len(self.commands)]
            self.command_index += 1

            cmd_msg = String()
            cmd_msg.data = command
            self.voice_pub.publish(cmd_msg)
            self.get_logger().info(f'Sent command: {command}')


def main(args=None):
    rclpy.init(args=args)

    simulator = VoiceSimulator()

    try:
        rclpy.spin(simulator)
    except KeyboardInterrupt:
        pass
    finally:
        simulator.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
```

## Step 5: Create a Launch File

Create a launch file to start all VLA components at `launch/vla_system.launch.py`:

```python
from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    # Command parser node
    command_parser = Node(
        package='vla_tutorial',
        executable='command_parser',
        name='command_parser',
        output='screen',
    )

    # VLA coordinator node
    vla_coordinator = Node(
        package='vla_tutorial',
        executable='vla_coordinator',
        name='vla_coordinator',
        output='screen',
    )

    # Voice simulator node (for testing)
    voice_simulator = Node(
        package='vla_tutorial',
        executable='voice_simulator',
        name='voice_simulator',
        output='screen',
    )

    ld = LaunchDescription()
    ld.add_action(command_parser)
    ld.add_action(vla_coordinator)
    ld.add_action(voice_simulator)

    return ld
```

## Step 6: Update Setup.py

Update the `setup.py` file to include the new executables:

```python
from setuptools import find_packages, setup

package_name = 'vla_tutorial'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', ['launch/vla_system.launch.py']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Your Name',
    maintainer_email='your.email@example.com',
    description='Vision-Language-Action tutorial',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'command_parser = vla_tutorial.command_parser:main',
            'vla_coordinator = vla_tutorial.vla_coordinator:main',
            'voice_simulator = vla_tutorial.voice_simulator:main',
        ],
    },
)
```

## Step 7: Build the Package

Build the VLA package:

```bash
cd ~/ros2_labs
source /opt/ros/humble/setup.bash
colcon build --packages-select vla_tutorial
source install/setup.bash
```

## Step 8: Run the Complete VLA System

First, make sure you have the simulation and perception systems running:

```bash
# Terminal 1: Start the simulation environment
cd ~/ros2_labs
source install/setup.bash
ros2 launch robot_sim_description robot_sim.launch.py
```

```bash
# Terminal 2: Start the perception system
cd ~/ros2_labs
source install/setup.bash
ros2 launch perception_tutorial object_detection.launch.py
```

```bash
# Terminal 3: Start the VLA system
cd ~/ros2_labs
source install/setup.bash
ros2 launch vla_tutorial vla_system.launch.py
```

## Step 9: Monitor the System

In a fourth terminal, monitor the system's operation:

```bash
# Terminal 4: Monitor VLA feedback
cd ~/ros2_labs
source install/setup.bash
ros2 topic echo /vla_feedback

# Or monitor other topics
ros2 topic echo /parsed_command
ros2 topic echo /detected_objects
```

## Step 10: Send Manual Commands

You can also send manual commands to test the system:

```bash
# Send a manual command
cd ~/ros2_labs
source install/setup.bash
ros2 topic pub /voice_command std_msgs/String "data: 'go to the red object'"

# Or send other commands
ros2 topic pub /voice_command std_msgs/String "data: 'find the blue object'"
```

## Step 11: Create a Simple Test Node

Create a simple test node to evaluate the system at `vla_tutorial/test_vla.py`:

```python
#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import Twist


class VLATester(Node):
    def __init__(self):
        super().__init__('vla_tester')

        # Create publisher for commands
        self.command_pub = self.create_publisher(String, '/voice_command', 10)

        # Create subscriber for feedback
        self.feedback_sub = self.create_subscription(
            String,
            '/vla_feedback',
            self.feedback_callback,
            10
        )

        # Timer for sending test commands
        self.timer = self.create_timer(10.0, self.send_test_command)
        self.command_count = 0

        self.get_logger().info('VLA Tester initialized')

    def feedback_callback(self, msg):
        self.get_logger().info(f'VLA Feedback: {msg.data}')

    def send_test_command(self):
        commands = [
            "go to the red object",
            "move to the blue object",
            "find the green object",
        ]

        if self.command_count < len(commands):
            cmd = String()
            cmd.data = commands[self.command_count]
            self.command_pub.publish(cmd)
            self.get_logger().info(f'Sent test command: {cmd.data}')
            self.command_count += 1


def main(args=None):
    rclpy.init(args=args)

    tester = VLATester()

    try:
        rclpy.spin(tester)
    except KeyboardInterrupt:
        pass
    finally:
        tester.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
```

Add this to your setup.py:

```python
entry_points={
    'console_scripts': [
        'command_parser = vla_tutorial.command_parser:main',
        'vla_coordinator = vla_tutorial.vla_coordinator:main',
        'voice_simulator = vla_tutorial.voice_simulator:main',
        'test_vla = vla_tutorial.test_vla:main',
    ],
},
```

## Step 12: Rebuild and Test

```bash
cd ~/ros2_labs
source /opt/ros/humble/setup.bash
colcon build --packages-select vla_tutorial
source install/setup.bash

# Run the complete system
# Terminal 1: Simulation
ros2 launch robot_sim_description robot_sim.launch.py

# Terminal 2: Perception
ros2 launch perception_tutorial object_detection.launch.py

# Terminal 3: VLA System
ros2 launch vla_tutorial vla_system.launch.py

# Terminal 4: VLA Tester
ros2 run vla_tutorial test_vla
```

## Expected Results

- The VLA system should parse natural language commands
- The system should identify target colored objects using the perception system
- The robot should navigate toward the specified colored object
- Feedback messages should indicate the system's state
- The robot should stop when it gets close to the target object

## Troubleshooting

### Common Issues

**Issue**: "No module named 'cv2'" or "No module named 'numpy'"
**Solution**: Install OpenCV and NumPy:
```bash
pip install opencv-python numpy
```

**Issue**: Nodes can't communicate
**Solution**: Verify all topics match between publishers and subscribers

**Issue**: Robot doesn't move toward objects
**Solution**: Check that perception system is running and publishing object detections

**Issue**: Commands not being parsed correctly
**Solution**: Check that voice command format matches the patterns in the parser

## Understanding the Implementation

### VLA Architecture
- **Language Component**: Command parser processes natural language
- **Vision Component**: Reuses perception system for object detection
- **Action Component**: Navigation system executes movement commands
- **Integration**: Coordinator node manages the flow between components

### Command Flow
1. Natural language command received
2. Command parsed into structured format
3. Target object identified in visual scene
4. Navigation plan executed to reach target
5. Feedback provided to user

### ROS 2 Integration
- Proper message types for each component
- Topic-based communication between components
- Modular design allowing components to run independently

## Extensions

To extend this basic VLA implementation:

1. **Add Grasping**: Implement manipulation actions beyond navigation
2. **Improve Language Understanding**: Use more sophisticated NLP models
3. **Add Safety Checks**: Implement collision avoidance during navigation
4. **Integrate LLMs**: Use large language models for better command understanding

## Assessment

To verify you've completed this lab successfully:
1. The system parses natural language commands correctly
2. The robot navigates toward specified colored objects
3. The system provides feedback during operation
4. All components communicate properly through ROS 2 topics

## Sim-to-Real Connection

The same VLA principles used in this simulation will apply to real robots:
- Language understanding remains the same
- Navigation algorithms transfer directly
- The main differences will be in perception quality and environmental conditions

Congratulations! You've implemented a basic Vision-Language-Action system that demonstrates the integration of perception, language understanding, and action execution.