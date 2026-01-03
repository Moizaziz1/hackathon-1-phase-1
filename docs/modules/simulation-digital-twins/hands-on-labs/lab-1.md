---
sidebar_label: 'Lab 1: Basic Robot Simulation'
sidebar_position: 1
---

# Lab 1: Basic Robot Simulation

In this lab, you'll create your first robot simulation using Gazebo and ROS 2. You'll build a simple differential drive robot, simulate it in a virtual environment, and control it using ROS 2 commands.

## Learning Objectives

After completing this lab, you will be able to:
- Create a basic robot model in URDF format
- Set up a Gazebo simulation environment
- Integrate the robot model with ROS 2
- Control the robot in simulation using ROS 2 commands
- Monitor sensor data from the simulated robot

## Prerequisites

Before starting this lab, ensure you have:
- Completed the ROS 2 Fundamentals module and lab
- Successfully installed ROS 2 Humble Hawksbill
- Gazebo installed (typically included with desktop-full installation)
- Basic understanding of URDF robot description format

## Step 1: Create a Robot Description Package

First, create a new ROS 2 package for your robot model:

```bash
cd ~/ros2_labs/src
ros2 pkg create --build-type ament_cmake robot_sim_description
```

## Step 2: Create the URDF Model

Create the directory structure for your robot model:

```bash
cd ~/ros2_labs/src/robot_sim_description
mkdir -p urdf meshes config launch
```

Create the main robot URDF file at `urdf/simple_robot.urdf`:

```xml
<?xml version="1.0"?>
<robot name="simple_robot" xmlns:xacro="http://www.ros.org/wiki/xacro">

  <!-- Base link -->
  <link name="base_link">
    <visual>
      <geometry>
        <box size="0.5 0.3 0.15"/>
      </geometry>
      <material name="blue">
        <color rgba="0 0 1 0.8"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <box size="0.5 0.3 0.15"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="1.0"/>
      <inertia ixx="0.01" ixy="0.0" ixz="0.0" iyy="0.01" iyz="0.0" izz="0.01"/>
    </inertial>
  </link>

  <!-- Left wheel -->
  <link name="left_wheel">
    <visual>
      <geometry>
        <cylinder radius="0.1" length="0.05"/>
      </geometry>
      <material name="black">
        <color rgba="0 0 0 1"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <cylinder radius="0.1" length="0.05"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="0.1"/>
      <inertia ixx="0.001" ixy="0.0" ixz="0.0" iyy="0.001" iyz="0.0" izz="0.001"/>
    </inertial>
  </link>

  <!-- Right wheel -->
  <link name="right_wheel">
    <visual>
      <geometry>
        <cylinder radius="0.1" length="0.05"/>
      </geometry>
      <material name="black">
        <color rgba="0 0 0 1"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <cylinder radius="0.1" length="0.05"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="0.1"/>
      <inertia ixx="0.001" ixy="0.0" ixz="0.0" iyy="0.001" iyz="0.0" izz="0.001"/>
    </inertial>
  </link>

  <!-- Base to left wheel joint -->
  <joint name="left_wheel_joint" type="continuous">
    <parent link="base_link"/>
    <child link="left_wheel"/>
    <origin xyz="0 0.2 0" rpy="1.5708 0 0"/>
    <axis xyz="0 0 1"/>
  </joint>

  <!-- Base to right wheel joint -->
  <joint name="right_wheel_joint" type="continuous">
    <parent link="base_link"/>
    <child link="right_wheel"/>
    <origin xyz="0 -0.2 0" rpy="1.5708 0 0"/>
    <axis xyz="0 0 1"/>
  </joint>

  <!-- Camera sensor -->
  <link name="camera_link">
    <visual>
      <geometry>
        <box size="0.05 0.05 0.05"/>
      </geometry>
      <material name="red">
        <color rgba="1 0 0 0.8"/>
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
    <parent link="base_link"/>
    <child link="camera_link"/>
    <origin xyz="0.25 0 0.05"/>
  </joint>

</robot>
```

## Step 3: Add Gazebo Integration

Create a Gazebo-specific URDF file at `urdf/simple_robot.gazebo.xacro`:

```xml
<?xml version="1.0"?>
<robot xmlns:xacro="http://www.ros.org/wiki/xacro">

  <!-- Gazebo materials -->
  <gazebo reference="base_link">
    <material>Gazebo/Blue</material>
  </gazebo>

  <gazebo reference="left_wheel">
    <material>Gazebo/Black</material>
  </gazebo>

  <gazebo reference="right_wheel">
    <material>Gazebo/Black</material>
  </gazebo>

  <gazebo reference="camera_link">
    <material>Gazebo/Red</material>
  </gazebo>

  <!-- Differential drive plugin -->
  <gazebo>
    <plugin name="diff_drive" filename="libgazebo_ros_diff_drive.so">
      <ros>
        <namespace>/simple_robot</namespace>
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
          <namespace>/simple_robot</namespace>
          <remapping>image_raw:=camera/image_raw</remapping>
          <remapping>camera_info:=camera/camera_info</remapping>
        </ros>
        <frame_name>camera_link_optical</frame_name>
      </plugin>
    </sensor>
  </gazebo>

</robot>
```

## Step 4: Create a Combined Robot File

Create a file that combines the base URDF and Gazebo extensions at `urdf/robot.xacro`:

```xml
<?xml version="1.0"?>
<robot name="simple_robot" xmlns:xacro="http://www.ros.org/wiki/xacro">

  <!-- Include the base robot description -->
  <xacro:include filename="simple_robot.urdf"/>

  <!-- Include Gazebo-specific extensions -->
  <xacro:include filename="simple_robot.gazebo.xacro"/>

  <!-- Add optical frame for camera -->
  <joint name="camera_optical_joint" type="fixed">
    <parent link="camera_link"/>
    <child link="camera_link_optical"/>
    <origin xyz="0 0 0" rpy="-1.5708 0 -1.5708"/>
  </joint>

  <link name="camera_link_optical"/>

</robot>
```

## Step 5: Create a Launch File

Create a launch file at `launch/robot_sim.launch.py`:

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
                FindPackageShare('robot_sim_description'),
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
            '-entity', 'simple_robot',
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

## Step 6: Update Package Configuration

Update the `CMakeLists.txt` file in your package:

```cmake
cmake_minimum_required(VERSION 3.8)
project(robot_sim_description)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(xacro REQUIRED)

# Install launch files
install(DIRECTORY launch
  DESTINATION share/${PROJECT_NAME}
)

# Install URDF files
install(DIRECTORY urdf
  DESTINATION share/${PROJECT_NAME}
)

# Install config files
install(DIRECTORY config
  DESTINATION share/${PROJECT_NAME}
)

# Install meshes files
install(DIRECTORY meshes
  DESTINATION share/${PROJECT_NAME}
)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
```

Update the `package.xml` file:

```xml
<?xml version="1.0"?>
<?xml-model href="http://download.ros.org/schema/package_format3.xsd" schematypens="http://www.w3.org/2001/XMLSchema"?>
<package format="3">
  <name>robot_sim_description</name>
  <version>0.0.0</version>
  <description>Simple robot model for simulation</description>
  <maintainer email="your.email@example.com">Your Name</maintainer>
  <license>Apache-2.0</license>

  <buildtool_depend>ament_cmake</buildtool_depend>

  <depend>gazebo_ros</depend>
  <depend>gazebo_plugins</depend>
  <depend>robot_state_publisher</depend>
  <depend>xacro</depend>

  <test_depend>ament_lint_auto</test_depend>
  <test_depend>ament_lint_common</test_depend>

  <export>
    <build_type>ament_cmake</build_type>
  </export>
</package>
```

## Step 7: Build the Package

Build your package:

```bash
cd ~/ros2_labs
source /opt/ros/humble/setup.bash
colcon build --packages-select robot_sim_description
```

## Step 8: Launch the Simulation

Launch the simulation:

```bash
cd ~/ros2_labs
source install/setup.bash
ros2 launch robot_sim_description robot_sim.launch.py
```

This will start Gazebo with your robot model in the world.

## Step 9: Control the Robot

Open a new terminal and source the workspace:

```bash
cd ~/ros2_labs
source install/setup.bash
```

Publish velocity commands to control the robot:

```bash
# Move forward
ros2 topic pub /simple_robot/cmd_vel geometry_msgs/msg/Twist '{linear: {x: 0.5}, angular: {z: 0.0}}'

# Rotate in place
ros2 topic pub /simple_robot/cmd_vel geometry_msgs/msg/Twist '{linear: {x: 0.0}, angular: {z: 0.5}}'

# Stop the robot
ros2 topic pub /simple_robot/cmd_vel geometry_msgs/msg/Twist '{linear: {x: 0.0}, angular: {z: 0.0}}'
```

## Step 10: Monitor Sensor Data

Monitor the camera data:

```bash
# Check available topics
ros2 topic list | grep simple_robot

# View camera info
ros2 topic echo /simple_robot/camera/camera_info

# View odometry data
ros2 topic echo /simple_robot/odom
```

## Step 11: Create a Simple Controller Node

Create a Python script to automatically control the robot. Create the file `robot_sim_description/simple_controller.py`:

```python
#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
import math


class SimpleController(Node):
    def __init__(self):
        super().__init__('simple_controller')

        # Create publisher for velocity commands
        self.cmd_vel_pub = self.create_publisher(Twist, '/simple_robot/cmd_vel', 10)

        # Create subscriber for odometry
        self.odom_sub = self.create_subscription(
            Odometry,
            '/simple_robot/odom',
            self.odom_callback,
            10
        )

        # Timer for control loop
        self.timer = self.create_timer(0.1, self.control_loop)

        # State variables
        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0
        self.target_x = 2.0
        self.target_y = 2.0
        self.reached_target = False

        self.get_logger().info('Simple Controller node initialized')

    def odom_callback(self, msg):
        # Extract position and orientation from odometry
        self.x = msg.pose.pose.position.x
        self.y = msg.pose.pose.position.y

        # Extract orientation (simplified - assuming z-axis rotation only)
        q = msg.pose.pose.orientation
        self.theta = math.atan2(2.0 * (q.w * q.z + q.x * q.y),
                                1.0 - 2.0 * (q.y * q.y + q.z * q.z))

    def control_loop(self):
        if self.reached_target:
            # Stop the robot when target is reached
            cmd = Twist()
            self.cmd_vel_pub.publish(cmd)
            return

        # Calculate distance to target
        dx = self.target_x - self.x
        dy = self.target_y - self.y
        distance = math.sqrt(dx * dx + dy * dy)

        # Calculate target angle
        target_angle = math.atan2(dy, dx)

        # Calculate angle difference
        angle_diff = target_angle - self.theta
        # Normalize angle to [-pi, pi]
        while angle_diff > math.pi:
            angle_diff -= 2.0 * math.pi
        while angle_diff < -math.pi:
            angle_diff += 2.0 * math.pi

        cmd = Twist()

        if distance > 0.1:  # If not close to target
            # Proportional controller for rotation
            cmd.angular.z = max(min(angle_diff * 1.0, 0.5), -0.5)

            # Move forward when roughly aligned
            if abs(angle_diff) < 0.2:
                cmd.linear.x = min(distance * 0.5, 0.5)
        else:
            # Reached target
            self.reached_target = True
            self.get_logger().info(f'Reached target at ({self.target_x}, {self.target_y})')

        self.cmd_vel_pub.publish(cmd)


def main(args=None):
    rclpy.init(args=args)

    controller = SimpleController()

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

## Step 12: Update Setup.py for the Controller

Add the controller to your `setup.py`:

```python
from setuptools import find_packages, setup

package_name = 'robot_sim_description'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Your Name',
    maintainer_email='your.email@example.com',
    description='Simple robot model for simulation',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'simple_controller = robot_sim_description.simple_controller:main',
        ],
    },
)
```

## Step 13: Build and Run the Controller

Rebuild the package and run the controller:

```bash
cd ~/ros2_labs
source /opt/ros/humble/setup.bash
colcon build --packages-select robot_sim_description
source install/setup.bash

# In one terminal, start the simulation
ros2 launch robot_sim_description robot_sim.launch.py

# In another terminal, run the controller
ros2 run robot_sim_description simple_controller
```

## Expected Results

- Your robot should appear in the Gazebo simulation
- You should be able to control it using ROS 2 topics
- The robot should have a camera sensor that publishes data
- The simple controller should move the robot to a target location

## Troubleshooting

### Common Issues

**Issue**: Robot doesn't appear in Gazebo
**Solution**: Check that the spawn_entity node is working and the URDF is valid

**Issue**: Can't control the robot
**Solution**: Verify topic names and that the differential drive plugin is loaded correctly

**Issue**: No sensor data
**Solution**: Check sensor plugin configuration and topic names

**Issue**: Build fails
**Solution**: Make sure all dependencies are installed: `sudo apt install ros-humble-gazebo-ros ros-humble-gazebo-plugins`

## Understanding the Implementation

### URDF Structure
- Links define the physical parts of the robot
- Joints define how parts connect and move
- Visual and collision properties define appearance and physics

### Gazebo Integration
- Plugins provide simulation-specific functionality
- The differential drive plugin enables ROS 2 control
- Sensor plugins simulate real sensors

### Launch File
- Coordinates starting multiple nodes
- Handles parameter configuration
- Manages the simulation environment

## Sim-to-Real Connection

The same ROS 2 interfaces used in simulation can be used with real robots. The key differences are:
- Simulation: Perfect sensing, no communication delays
- Reality: Sensor noise, communication delays, hardware limitations
- The control algorithms remain the same, but may need tuning for real hardware

## Assessment

To verify you've completed this lab successfully:
1. You can launch the simulation with your robot model
2. You can control the robot using ROS 2 commands
3. You can monitor sensor data from the robot
4. You can run the simple controller to autonomously navigate

Congratulations! You've created your first robot simulation with ROS 2 and Gazebo.