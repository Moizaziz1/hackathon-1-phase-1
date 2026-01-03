---
sidebar_label: 'Implementation Guide'
sidebar_position: 3
---

# Capstone Project: Implementation Guide

This guide provides a step-by-step approach to implementing the Autonomous Humanoid Robot system. Follow these steps in order to build a complete, functional system.

## Implementation Phases

The implementation is organized into 5 phases, each building upon the previous one:

1. **Foundation Setup** - Basic ROS 2 architecture and simulation environment
2. **Perception System** - Object detection, mapping, and localization
3. **Navigation System** - Path planning and obstacle avoidance
4. **Manipulation System** - Motion planning and grasping
5. **Integration & Task Planning** - High-level control and natural language processing

## Phase 1: Foundation Setup

### Step 1.1: Create Project Structure

Create the main project package:

```bash
cd ~/ros2_labs/src
ros2 pkg create --build-type ament_python humanoid_robot_system
cd humanoid_robot_system
mkdir -p humanoid_robot_system launch config worlds
```

### Step 1.2: Create Robot Model

Create a simple humanoid robot URDF at `urdf/humanoid_robot.urdf`:

```xml
<?xml version="1.0"?>
<robot name="humanoid_robot" xmlns:xacro="http://www.ros.org/wiki/xacro">

  <!-- Base link -->
  <link name="base_link">
    <visual>
      <geometry>
        <box size="0.6 0.4 0.3"/>
      </geometry>
      <material name="blue">
        <color rgba="0 0 1 0.8"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <box size="0.6 0.4 0.3"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="10.0"/>
      <inertia ixx="0.1" ixy="0.0" ixz="0.0" iyy="0.1" iyz="0.0" izz="0.1"/>
    </inertial>
  </link>

  <!-- Head -->
  <link name="head">
    <visual>
      <geometry>
        <sphere radius="0.1"/>
      </geometry>
      <material name="white">
        <color rgba="1 1 1 0.8"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <sphere radius="0.1"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="0.5"/>
      <inertia ixx="0.001" ixy="0.0" ixz="0.0" iyy="0.001" iyz="0.0" izz="0.001"/>
    </inertial>
  </link>

  <joint name="head_joint" type="fixed">
    <parent link="base_link"/>
    <child link="head"/>
    <origin xyz="0 0 0.25"/>
  </joint>

  <!-- Camera in head -->
  <link name="camera_link">
    <visual>
      <geometry>
        <box size="0.05 0.05 0.05"/>
      </geometry>
      <material name="black">
        <color rgba="0 0 0 1"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <box size="0.05 0.05 0.05"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="0.01"/>
      <inertia ixx="0.0001" ixy="0.0" ixz="0.0" iyy="0.0001" iyz="0.0" izz="0.0001"/>
    </inertial>
  </link>

  <joint name="camera_joint" type="fixed">
    <parent link="head"/>
    <child link="camera_link"/>
    <origin xyz="0.05 0 0"/>
  </joint>

  <!-- Left arm base -->
  <link name="left_arm_base">
    <visual>
      <geometry>
        <box size="0.1 0.1 0.1"/>
      </geometry>
      <material name="gray">
        <color rgba="0.5 0.5 0.5 0.8"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <box size="0.1 0.1 0.1"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="0.2"/>
      <inertia ixx="0.0001" ixy="0.0" ixz="0.0" iyy="0.0001" iyz="0.0" izz="0.0001"/>
    </inertial>
  </link>

  <joint name="left_arm_joint" type="fixed">
    <parent link="base_link"/>
    <child link="left_arm_base"/>
    <origin xyz="0.2 0.15 0"/>
  </joint>

  <!-- Right arm base -->
  <link name="right_arm_base">
    <visual>
      <geometry>
        <box size="0.1 0.1 0.1"/>
      </geometry>
      <material name="gray">
        <color rgba="0.5 0.5 0.5 0.8"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <box size="0.1 0.1 0.1"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="0.2"/>
      <inertia ixx="0.0001" ixy="0.0" ixz="0.0" iyy="0.0001" iyz="0.0" izz="0.0001"/>
    </inertial>
  </link>

  <joint name="right_arm_joint" type="fixed">
    <parent link="base_link"/>
    <child link="right_arm_base"/>
    <origin xyz="0.2 -0.15 0"/>
  </joint>

</robot>
```

### Step 1.3: Create Gazebo Integration

Create `urdf/humanoid_robot.gazebo.xacro`:

```xml
<?xml version="1.0"?>
<robot xmlns:xacro="http://www.ros.org/wiki/xacro">

  <!-- Gazebo materials -->
  <gazebo reference="base_link">
    <material>Gazebo/Blue</material>
  </gazebo>

  <gazebo reference="head">
    <material>Gazebo/White</material>
  </gazebo>

  <gazebo reference="camera_link">
    <material>Gazebo/Black</material>
  </gazebo>

  <gazebo reference="left_arm_base">
    <material>Gazebo/Grey</material>
  </gazebo>

  <gazebo reference="right_arm_base">
    <material>Gazebo/Grey</material>
  </gazebo>

  <!-- Differential drive plugin -->
  <gazebo>
    <plugin name="diff_drive" filename="libgazebo_ros_diff_drive.so">
      <ros>
        <namespace>/humanoid_robot</namespace>
        <remapping>cmd_vel:=cmd_vel</remapping>
        <remapping>odom:=odom</remapping>
      </ros>
      <update_rate>30</update_rate>
      <left_joint>left_wheel_joint</left_joint>
      <right_joint>right_wheel_joint</right_joint>
      <wheel_separation>0.4</wheel_separation>
      <wheel_diameter>0.2</wheel_diameter>
      <max_wheel_torque>20</max_wheel_torque>
      <max_wheel_acceleration>1.0</max_wheel_acceleration>
      <publish_odom>true</publish_odom>
      <publish_odom_tf>true</publish_odom_tf>
      <publish_wheel_tf>true</publish_wheel_tf>
      <odometry_frame>odom</odometry_frame>
      <robot_base_frame>base_link</robot_base_frame>
    </plugin>
  </gazebo>

  <!-- Camera sensor plugin -->
  <gazebo reference="camera_link">
    <sensor name="camera" type="camera">
      <update_rate>30</update_rate>
      <camera name="head">
        <horizontal_fov>1.089</horizontal_fov>
        <image>
          <width>640</width>
          <height>480</height>
          <format>R8G8B8</format>
        </image>
        <clip>
          <near>0.05</near>
          <far>3</far>
        </clip>
      </camera>
      <plugin name="camera_controller" filename="libgazebo_ros_camera.so">
        <ros>
          <namespace>/humanoid_robot</namespace>
          <remapping>image_raw:=camera/image_raw</remapping>
          <remapping>camera_info:=camera/camera_info</remapping>
        </ros>
        <frame_name>camera_link_optical</frame_name>
      </plugin>
    </sensor>
  </gazebo>

</robot>
```

### Step 1.4: Create Combined Robot File

Create `urdf/robot.xacro`:

```xml
<?xml version="1.0"?>
<robot name="humanoid_robot" xmlns:xacro="http://www.ros.org/wiki/xacro">

  <!-- Include the base robot description -->
  <xacro:include filename="humanoid_robot.urdf"/>

  <!-- Include Gazebo-specific extensions -->
  <xacro:include filename="humanoid_robot.gazebo.xacro"/>

  <!-- Add optical frame for camera -->
  <joint name="camera_optical_joint" type="fixed">
    <parent link="camera_link"/>
    <child link="camera_link_optical"/>
    <origin xyz="0 0 0" rpy="-1.5708 0 -1.5708"/>
  </joint>

  <link name="camera_link_optical"/>

</robot>
```

### Step 1.5: Create Simulation Launch File

Create `launch/simulation.launch.py`:

```python
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    # Launch configuration variables
    use_sim_time = LaunchConfiguration('use_sim_time')
    world = LaunchConfiguration('world')

    # Declare launch arguments
    declare_use_sim_time = DeclareLaunchArgument(
        'use_sim_time',
        default_value='true',
        description='Use simulation (Gazebo) clock if true'
    )

    declare_world = DeclareLaunchArgument(
        'world',
        default_value='empty.sdf',
        description='Choose one of the world files from `/usr/share/gazebo-11/worlds`'
    )

    # Start Gazebo server
    gzserver = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                FindPackageShare('gazebo_ros'),
                'launch',
                'gzserver.launch.py'
            ])
        ]),
        launch_arguments={
            'world': world,
            'verbose': 'false',
        }.items()
    )

    # Start Gazebo client
    gzclient = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                FindPackageShare('gazebo_ros'),
                'launch',
                'gzclient.launch.py'
            ])
        ])
    )

    # Publish robot state
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{
            'use_sim_time': use_sim_time,
            'robot_description': open(PathJoinSubstitution([
                FindPackageShare('humanoid_robot_system'),
                'urdf',
                'robot.xacro'
            ]).perform({})).read()
        }]
    )

    # Spawn robot in Gazebo
    spawn_entity = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=[
            '-topic', 'robot_description',
            '-entity', 'humanoid_robot',
            '-x', '0.0',
            '-y', '0.0',
            '-z', '0.1'
        ],
        output='screen'
    )

    # Create launch description and add actions
    ld = LaunchDescription()

    ld.add_action(declare_use_sim_time)
    ld.add_action(declare_world)
    ld.add_action(gzserver)
    ld.add_action(gzclient)
    ld.add_action(robot_state_publisher)
    ld.add_action(spawn_entity)

    return ld
```

### Step 1.6: Create Basic Control Node

Create `humanoid_robot_system/base_controller.py`:

```python
#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import String
import time


class BaseController(Node):
    def __init__(self):
        super().__init__('base_controller')

        # Create publisher for velocity commands
        self.cmd_vel_pub = self.create_publisher(Twist, '/humanoid_robot/cmd_vel', 10)

        # Create subscriber for voice commands
        self.voice_sub = self.create_subscription(
            String,
            '/voice_command',
            self.voice_callback,
            10
        )

        # Timer for control loop
        self.timer = self.create_timer(0.1, self.control_loop)

        # State variables
        self.current_command = None
        self.command_time = None
        self.command_duration = 3.0  # seconds

        self.get_logger().info('Base Controller initialized')

    def voice_callback(self, msg):
        command = msg.data.lower()
        self.get_logger().info(f'Received voice command: {command}')

        if 'forward' in command or 'go' in command:
            self.current_command = 'forward'
            self.command_time = time.time()
        elif 'backward' in command or 'back' in command:
            self.current_command = 'backward'
            self.command_time = time.time()
        elif 'left' in command:
            self.current_command = 'left'
            self.command_time = time.time()
        elif 'right' in command:
            self.current_command = 'right'
            self.command_time = time.time()
        elif 'stop' in command or 'halt' in command:
            self.current_command = 'stop'
            self.command_time = time.time()

    def control_loop(self):
        if self.current_command is None:
            return

        # Check if command has expired
        if time.time() - self.command_time > self.command_duration:
            self.current_command = None
            cmd = Twist()
            self.cmd_vel_pub.publish(cmd)
            return

        # Execute current command
        cmd = Twist()

        if self.current_command == 'forward':
            cmd.linear.x = 0.5
        elif self.current_command == 'backward':
            cmd.linear.x = -0.5
        elif self.current_command == 'left':
            cmd.angular.z = 0.5
        elif self.current_command == 'right':
            cmd.angular.z = -0.5
        elif self.current_command == 'stop':
            cmd.linear.x = 0.0
            cmd.angular.z = 0.0

        self.cmd_vel_pub.publish(cmd)


def main(args=None):
    rclpy.init(args=args)

    controller = BaseController()

    try:
        rclpy.spin(controller)
    except KeyboardInterrupt:
        pass
    finally:
        controller.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
```

### Step 1.7: Update Package Configuration

Update `setup.py`:

```python
from setuptools import find_packages, setup

package_name = 'humanoid_robot_system'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', ['launch/simulation.launch.py']),
        ('share/' + package_name + '/urdf', [
            'urdf/humanoid_robot.urdf',
            'urdf/humanoid_robot.gazebo.xacro',
            'urdf/robot.xacro'
        ]),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Your Name',
    maintainer_email='your.email@example.com',
    description='Autonomous Humanoid Robot System',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'base_controller = humanoid_robot_system.base_controller:main',
        ],
    },
)
```

### Step 1.8: Build and Test Foundation

```bash
cd ~/ros2_labs
source /opt/ros/humble/setup.bash
colcon build --packages-select humanoid_robot_system
source install/setup.bash

# Test the simulation
ros2 launch humanoid_robot_system simulation.launch.py
```

## Phase 2: Perception System

### Step 2.1: Create Object Detection Node

Create `humanoid_robot_system/object_detector.py`:

```python
#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import String
from cv_bridge import CvBridge
import cv2
import numpy as np


class ObjectDetector(Node):
    def __init__(self):
        super().__init__('object_detector')

        # Create subscriber for camera images
        self.image_sub = self.create_subscription(
            Image,
            '/humanoid_robot/camera/image_raw',
            self.image_callback,
            10
        )

        # Create publisher for detected objects
        self.objects_pub = self.create_publisher(String, '/detected_objects', 10)

        # Initialize OpenCV bridge
        self.bridge = CvBridge()

        # Colors for object detection
        self.colors = {
            'red': ((0, 50, 50), (10, 255, 255)),
            'blue': ((100, 50, 50), (130, 255, 255)),
            'green': ((40, 50, 50), (80, 255, 255)),
        }

        self.get_logger().info('Object Detector initialized')

    def image_callback(self, msg):
        try:
            # Convert ROS image to OpenCV format
            cv_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")
        except Exception as e:
            self.get_logger().error(f'Could not convert image: {e}')
            return

        # Detect objects based on color
        detected_objects = []

        for color_name, (lower, upper) in self.colors.items():
            # Create mask for color range
            hsv = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(hsv, lower, upper)

            # Find contours
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # Filter contours by area
            for contour in contours:
                area = cv2.contourArea(contour)
                if area > 500:  # Minimum area threshold
                    # Calculate centroid
                    M = cv2.moments(contour)
                    if M["m00"] != 0:
                        cx = int(M["m10"] / M["m00"])
                        cy = int(M["m01"] / M["m00"])
                        detected_objects.append(f"{color_name}_object_at_{cx}_{cy}")

        # Publish detected objects
        if detected_objects:
            objects_msg = String()
            objects_msg.data = ','.join(detected_objects)
            self.objects_pub.publish(objects_msg)
            self.get_logger().info(f'Detected objects: {objects_msg.data}')


def main(args=None):
    rclpy.init(args=args)

    detector = ObjectDetector()

    try:
        rclpy.spin(detector)
    except KeyboardInterrupt:
        pass
    finally:
        detector.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
```

### Step 2.2: Update Setup.py for New Node

Add the new node to `setup.py`:

```python
entry_points={
    'console_scripts': [
        'base_controller = humanoid_robot_system.base_controller:main',
        'object_detector = humanoid_robot_system.object_detector:main',
    ],
},
```

### Step 2.3: Install Dependencies

```bash
pip3 install opencv-python cv-bridge
```

## Phase 3: Navigation System

### Step 3.1: Create Navigation Node

Create `humanoid_robot_system/navigation_manager.py`:

```python
#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist, PoseStamped
from nav_msgs.msg import Odometry
from std_msgs.msg import String
import math


class NavigationManager(Node):
    def __init__(self):
        super().__init__('navigation_manager')

        # Create publishers
        self.cmd_vel_pub = self.create_publisher(Twist, '/humanoid_robot/cmd_vel', 10)

        # Create subscribers
        self.odom_sub = self.create_subscription(
            Odometry,
            '/humanoid_robot/odom',
            self.odom_callback,
            10
        )

        self.nav_goal_sub = self.create_subscription(
            String,
            '/navigation_goal',
            self.nav_goal_callback,
            10
        )

        # Timer for navigation control
        self.timer = self.create_timer(0.1, self.navigation_loop)

        # State variables
        self.current_x = 0.0
        self.current_y = 0.0
        self.current_theta = 0.0
        self.goal_x = None
        self.goal_y = None
        self.navigating = False

        self.get_logger().info('Navigation Manager initialized')

    def odom_callback(self, msg):
        # Extract position and orientation from odometry
        self.current_x = msg.pose.pose.position.x
        self.current_y = msg.pose.pose.position.y

        # Extract orientation (simplified - assuming z-axis rotation only)
        q = msg.pose.pose.orientation
        self.current_theta = math.atan2(2.0 * (q.w * q.z + q.x * q.y),
                                       1.0 - 2.0 * (q.y * q.y + q.z * q.z))

    def nav_goal_callback(self, msg):
        try:
            # Parse goal coordinates from message (format: "x,y")
            coords = msg.data.split(',')
            self.goal_x = float(coords[0])
            self.goal_y = float(coords[1])
            self.navigating = True
            self.get_logger().info(f'Set navigation goal to: ({self.goal_x}, {self.goal_y})')
        except Exception as e:
            self.get_logger().error(f'Could not parse navigation goal: {e}')

    def navigation_loop(self):
        if not self.navigating or self.goal_x is None or self.goal_y is None:
            return

        # Calculate distance to goal
        dx = self.goal_x - self.current_x
        dy = self.goal_y - self.current_y
        distance = math.sqrt(dx * dx + dy * dy)

        # Calculate target angle
        target_angle = math.atan2(dy, dx)

        # Calculate angle difference
        angle_diff = target_angle - self.current_theta
        # Normalize angle to [-pi, pi]
        while angle_diff > math.pi:
            angle_diff -= 2.0 * math.pi
        while angle_diff < -math.pi:
            angle_diff += 2.0 * math.pi

        cmd = Twist()

        if distance > 0.2:  # If not close to goal
            # Proportional controller for rotation
            cmd.angular.z = max(min(angle_diff * 1.0, 0.5), -0.5)

            # Move forward when roughly aligned
            if abs(angle_diff) < 0.3:
                cmd.linear.x = min(distance * 0.5, 0.5)
        else:
            # Reached goal
            cmd.linear.x = 0.0
            cmd.angular.z = 0.0
            self.navigating = False
            self.get_logger().info(f'Reached navigation goal: ({self.goal_x}, {self.goal_y})')

        self.cmd_vel_pub.publish(cmd)


def main(args=None):
    rclpy.init(args=args)

    nav_manager = NavigationManager()

    try:
        rclpy.spin(nav_manager)
    except KeyboardInterrupt:
        pass
    finally:
        nav_manager.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
```

### Step 3.2: Update Setup.py

Add the navigation node to `setup.py`:

```python
entry_points={
    'console_scripts': [
        'base_controller = humanoid_robot_system.base_controller:main',
        'object_detector = humanoid_robot_system.object_detector:main',
        'navigation_manager = humanoid_robot_system.navigation_manager:main',
    ],
},
```

## Phase 4: Integration

### Step 4.1: Create Main System Controller

Create `humanoid_robot_system/system_controller.py`:

```python
#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import Twist
import re


class SystemController(Node):
    def __init__(self):
        super().__init__('system_controller')

        # Create publishers
        self.voice_cmd_pub = self.create_publisher(String, '/voice_command', 10)
        self.nav_goal_pub = self.create_publisher(String, '/navigation_goal', 10)
        self.cmd_vel_pub = self.create_publisher(Twwist, '/humanoid_robot/cmd_vel', 10)

        # Create subscriber for voice commands
        self.voice_input_sub = self.create_subscription(
            String,
            '/user_voice_input',
            self.voice_input_callback,
            10
        )

        self.get_logger().info('System Controller initialized')

    def voice_input_callback(self, msg):
        command = msg.data.lower()
        self.get_logger().info(f'Processing user command: {command}')

        # Parse navigation commands
        if 'go to' in command or 'navigate to' in command:
            self.parse_navigation_command(command)
        elif 'move to' in command:
            self.parse_navigation_command(command)
        else:
            # Forward other commands to base controller
            voice_cmd = String()
            voice_cmd.data = command
            self.voice_cmd_pub.publish(voice_cmd)

    def parse_navigation_command(self, command):
        # Simple parsing for coordinates in format like "go to x=2, y=3"
        x_match = re.search(r'x[=\s]*([+-]?\d*\.?\d+)', command)
        y_match = re.search(r'y[=\s]*([+-]?\d*\.?\d+)', command)

        if x_match and y_match:
            try:
                x = float(x_match.group(1))
                y = float(y_match.group(1))

                nav_goal = String()
                nav_goal.data = f"{x},{y}"
                self.nav_goal_pub.publish(nav_goal)

                self.get_logger().info(f'Navigating to: ({x}, {y})')
            except ValueError:
                self.get_logger().error('Could not parse coordinates')
        else:
            # If no coordinates found, try common locations
            if 'kitchen' in command:
                self.send_navigation_goal(3.0, 2.0)  # Example kitchen location
            elif 'living room' in command:
                self.send_navigation_goal(0.0, 0.0)  # Example living room location
            elif 'bedroom' in command:
                self.send_navigation_goal(-2.0, 3.0)  # Example bedroom location
            else:
                self.get_logger().info('Could not determine navigation goal from command')

    def send_navigation_goal(self, x, y):
        nav_goal = String()
        nav_goal.data = f"{x},{y}"
        self.nav_goal_pub.publish(nav_goal)
        self.get_logger().info(f'Navigating to: ({x}, {y})')


def main(args=None):
    rclpy.init(args=args)

    controller = SystemController()

    try:
        rclpy.spin(controller)
    except KeyboardInterrupt:
        pass
    finally:
        controller.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
```

### Step 4.2: Final Setup.py Update

```python
entry_points={
    'console_scripts': [
        'base_controller = humanoid_robot_system.base_controller:main',
        'object_detector = humanoid_robot_system.object_detector:main',
        'navigation_manager = humanoid_robot_system.navigation_manager:main',
        'system_controller = humanoid_robot_system.system_controller:main',
    ],
},
```

## Phase 5: Testing and Validation

### Step 5.1: Create Test Launch File

Create `launch/capstone_demo.launch.py`:

```python
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    # Launch Gazebo simulation
    simulation_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                FindPackageShare('humanoid_robot_system'),
                'launch',
                'simulation.launch.py'
            ])
        ])
    )

    # Launch base controller
    base_controller = Node(
        package='humanoid_robot_system',
        executable='base_controller',
        name='base_controller',
        output='screen'
    )

    # Launch object detector
    object_detector = Node(
        package='humanoid_robot_system',
        executable='object_detector',
        name='object_detector',
        output='screen'
    )

    # Launch navigation manager
    navigation_manager = Node(
        package='humanoid_robot_system',
        executable='navigation_manager',
        name='navigation_manager',
        output='screen'
    )

    # Launch system controller
    system_controller = Node(
        package='humanoid_robot_system',
        executable='system_controller',
        name='system_controller',
        output='screen'
    )

    ld = LaunchDescription()
    ld.add_action(simulation_launch)
    ld.add_action(base_controller)
    ld.add_action(object_detector)
    ld.add_action(navigation_manager)
    ld.add_action(system_controller)

    return ld
```

### Step 5.2: Build and Run Complete System

```bash
cd ~/ros2_labs
source /opt/ros/humble/setup.bash
colcon build --packages-select humanoid_robot_system
source install/setup.bash

# Launch the complete system
ros2 launch humanoid_robot_system capstone_demo.launch.py
```

### Step 5.3: Test the System

In a new terminal, send test commands:

```bash
# Navigate to specific coordinates
cd ~/ros2_labs
source install/setup.bash
ros2 topic pub /user_voice_input std_msgs/String "data: 'go to x=2 y=1'"

# Send basic movement commands
ros2 topic pub /user_voice_input std_msgs/String "data: 'go forward'"
ros2 topic pub /user_voice_input std_msgs/String "data: 'turn left'"
```

## Integration Points with Previous Modules

### ROS 2 Integration
- All nodes use standard ROS 2 communication patterns
- Proper topic and service naming conventions
- Parameter server for configuration

### Simulation Integration
- Robot model works in Gazebo simulation
- Sensor simulation provides realistic data
- Physics simulation for realistic movement

### Perception Integration
- Object detection node processes camera data
- Results published for other nodes to use
- Real-time processing capabilities

## Sim-to-Real Transfer Considerations

### Hardware Differences
- Simulation: Perfect sensing and control
- Reality: Sensor noise and control limitations
- Calibration requirements for real sensors

### Performance Tuning
- Adjust controller parameters for real hardware
- Consider computational limitations on robot
- Account for communication delays

### Safety Considerations
- Implement safety stops for real robot
- Add obstacle detection for collision avoidance
- Ensure human safety during operation

## Troubleshooting Common Issues

### Simulation Issues
- **Robot not appearing**: Check URDF validity and spawn parameters
- **No sensor data**: Verify plugin configuration and topic names
- **Control not working**: Check namespace and topic mappings

### ROS 2 Issues
- **Nodes not communicating**: Check topic names and namespaces
- **Performance issues**: Monitor CPU usage and optimize algorithms
- **Timing issues**: Adjust control loop frequencies

### Perception Issues
- **No object detection**: Check camera calibration and lighting
- **False detections**: Adjust threshold parameters
- **Processing lag**: Optimize image processing algorithms

## Assessment Criteria

Your implementation will be assessed on:
- **Functionality**: System performs basic navigation and object detection
- **Integration**: All components work together correctly
- **Code Quality**: Well-structured, documented, and maintainable code
- **Robustness**: Handles errors and edge cases appropriately
- **Documentation**: Clear explanations and usage instructions

## Next Steps

Once you have the basic system working:
1. Enhance the natural language processing capabilities
2. Add more sophisticated perception algorithms
3. Implement manipulation capabilities
4. Test in more complex environments
5. Optimize for real robot deployment

This implementation guide provides a solid foundation for your capstone project. The modular architecture allows for incremental development and testing, making it easier to debug and enhance individual components.