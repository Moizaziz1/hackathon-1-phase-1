---
sidebar_label: 'Lab 1: Basic Publisher/Subscriber'
sidebar_position: 1
---

# Lab 1: Basic Publisher/Subscriber

In this lab, you'll create your first ROS 2 publisher and subscriber nodes. This will give you hands-on experience with the fundamental communication pattern in ROS 2.

## Learning Objectives

After completing this lab, you will be able to:
- Create a basic ROS 2 package
- Implement a publisher node that sends messages
- Implement a subscriber node that receives messages
- Build and run your ROS 2 nodes
- Use ROS 2 command-line tools to monitor topics

## Prerequisites

Before starting this lab, ensure you have:
- Completed the setup guide
- Successfully installed ROS 2 Humble Hawksbill
- Set up your ROS 2 environment (`source /opt/ros/humble/setup.bash`)

## Step 1: Create a ROS 2 Package

First, create a new workspace and package for your lab:

```bash
# Create workspace directory
mkdir -p ~/ros2_labs/src
cd ~/ros2_labs

# Source ROS 2 environment
source /opt/ros/humble/setup.bash

# Create the package
ros2 pkg create --build-type ament_python beginner_py
```

## Step 2: Create the Publisher Node

Navigate to your package and create the publisher script:

```bash
cd ~/ros2_labs/src/beginner_py
mkdir -p beginner_py
```

Create the publisher file at `beginner_py/talker.py`:

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(String, 'topic', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        msg = String()
        msg.data = 'Hello World: %d' % self.i
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.data)
        self.i += 1


def main(args=None):
    rclpy.init(args=args)

    minimal_publisher = MinimalPublisher()

    rclpy.spin(minimal_publisher)

    # Destroy the node explicitly
    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
```

## Step 3: Create the Subscriber Node

Create the subscriber file at `beginner_py/listener.py`:

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class MinimalSubscriber(Node):

    def __init__(self):
        super().__init__('minimal_subscriber')
        self.subscription = self.create_subscription(
            String,
            'topic',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        self.get_logger().info('I heard: "%s"' % msg.data)


def main(args=None):
    rclpy.init(args=args)

    minimal_subscriber = MinimalSubscriber()

    rclpy.spin(minimal_subscriber)

    # Destroy the node explicitly
    minimal_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
```

## Step 4: Update the Package Configuration

Update the `setup.py` file in your package directory to make the scripts executable:

```python
from setuptools import find_packages, setup

package_name = 'beginner_py'

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
    description='Beginner Python package for ROS 2',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'talker = beginner_py.talker:main',
            'listener = beginner_py.listener:main',
        ],
    },
)
```

## Step 5: Build the Package

Go back to your workspace root and build the package:

```bash
cd ~/ros2_labs
source /opt/ros/humble/setup.bash
colcon build --packages-select beginner_py
```

## Step 6: Source the Workspace

```bash
source install/setup.bash
```

## Step 7: Run the Publisher and Subscriber

Open two terminal windows:

**Terminal 1** (Publisher):
```bash
cd ~/ros2_labs
source install/setup.bash
ros2 run beginner_py talker
```

**Terminal 2** (Subscriber):
```bash
cd ~/ros2_labs
source install/setup.bash
ros2 run beginner_py listener
```

You should see the publisher sending messages and the subscriber receiving them.

## Step 8: Use ROS 2 Command-Line Tools

While your nodes are running, open a third terminal and try these commands:

```bash
# List all topics
ros2 topic list

# Echo messages from the topic
ros2 topic echo /topic std_msgs/msg/String

# Show topic information
ros2 topic info /topic

# Show connection information
ros2 node info /minimal_publisher
ros2 node info /minimal_subscriber
```

## Step 9: Experiment with Parameters

You can also modify the publishing rate by changing the timer period in the publisher code and rebuilding:

```bash
# After making changes
cd ~/ros2_labs
colcon build --packages-select beginner_py
source install/setup.bash
```

## Expected Results

- Publisher should output: `Publishing: "Hello World: X"` (where X is increasing)
- Subscriber should output: `I heard: "Hello World: X"`
- Messages should be transmitted approximately every 0.5 seconds

## Troubleshooting

### Common Issues

**Issue**: "Command 'ros2' not found"
**Solution**: Make sure you've sourced the ROS 2 environment: `source /opt/ros/humble/setup.bash`

**Issue**: Nodes can't communicate
**Solution**: Check that both terminals have sourced the workspace: `source install/setup.bash`

**Issue**: Build fails
**Solution**: Ensure you're in the workspace root directory when running colcon build

## Understanding the Code

### Publisher Code
- Creates a publisher on the 'topic' with String message type
- Uses a timer to publish messages every 0.5 seconds
- Increments a counter and includes it in the message

### Subscriber Code
- Creates a subscription to the 'topic' with String message type
- Callback function processes incoming messages
- Logs the received message content

## Next Steps

This lab introduced the fundamental ROS 2 communication pattern. In future labs, you'll explore:
- Services for request/response communication
- Actions for long-running tasks
- Parameters for configuration
- TF for coordinate transformations

## Sim-to-Real Connection

The publisher/subscriber pattern you've learned is identical in simulation and on real robots. The same code structure will work with real sensors and actuators, with the only difference being the data source (simulated vs. real hardware).

## Assessment

To verify you've completed this lab successfully:
1. You can run both nodes simultaneously
2. Messages are successfully transmitted from publisher to subscriber
3. You can use ROS 2 command-line tools to monitor the communication
4. You understand the basic structure of ROS 2 Python nodes

Congratulations! You've created your first ROS 2 publisher and subscriber nodes.