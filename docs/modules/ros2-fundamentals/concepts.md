---
sidebar_label: 'Core Concepts'
sidebar_position: 1
---

# ROS 2 Core Concepts

This section covers the fundamental concepts of ROS 2 architecture and how to work with its core components.

## Architecture Overview

ROS 2 is designed around a distributed system architecture where multiple processes (nodes) communicate with each other through a publish/subscribe model, services, and actions.

### Nodes

A node is an executable that uses ROS 2 to communicate with other nodes. Nodes are the fundamental building blocks of a ROS 2 system.

```python
# Example ROS 2 Node in Python
import rclpy
from rclpy.node import Node

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
```

### Topics and Messages

Topics are named buses over which nodes exchange messages. The publish/subscribe paradigm allows for asynchronous communication between nodes.

- **Publisher**: A node that sends messages to a topic
- **Subscriber**: A node that receives messages from a topic
- **Message Types**: Defined schemas for data exchange (e.g., std_msgs/String, sensor_msgs/LaserScan)

### Services

Services provide synchronous request/response communication between nodes. A service has a client and a server.

```python
# Example ROS 2 Service
from example_interfaces.srv import AddTwoInts

def add_two_ints_callback(request, response):
    response.sum = request.a + request.b
    return response

service = node.create_service(AddTwoInts, 'add_two_ints', add_two_ints_callback)
```

### Actions

Actions are used for long-running tasks that may provide feedback during execution. They have a goal, result, and feedback mechanism.

## Communication Patterns

### Publisher/Subscriber (Topics)
- Asynchronous communication
- Multiple publishers and subscribers can exist for the same topic
- Data is sent to all subscribers simultaneously

### Client/Server (Services)
- Synchronous request/response
- Request-response pattern
- Used for operations that return a result immediately

### Action Client/Server
- For long-running tasks
- Provides feedback during execution
- Supports goal preemption

## Launch Files

Launch files allow you to start multiple nodes at once with specific configurations:

```xml
<!-- Example launch file -->
<launch>
  <node pkg="demo_nodes_py" exec="talker" name="my_publisher"/>
  <node pkg="demo_nodes_py" exec="listener" name="my_subscriber"/>
</launch>
```

## Parameter Server

ROS 2 provides a parameter server for runtime configuration of nodes. Parameters can be:
- Declared within nodes
- Set at launch time
- Modified during runtime

## TF (Transforms)

TF is a package that keeps track of coordinate frames in a tree structure over time. It's essential for robotics applications involving multiple sensors and coordinate systems.

## Quality of Service (QoS)

QoS settings allow you to control the behavior of communication between nodes, including reliability, durability, and history policies.

## ROS 2 Tools

### Command Line Tools
- `ros2 run`: Run a node
- `ros2 topic`: Interact with topics
- `ros2 service`: Interact with services
- `ros2 action`: Interact with actions
- `ros2 node`: Interact with nodes
- `ros2 param`: Interact with parameters
- `ros2 launch`: Launch multiple nodes

### Visualization Tools
- `rqt`: General-purpose GUI for ROS
- `rviz2`: 3D visualization tool for displaying sensor data and robot state

## Best Practices

1. **Node Design**: Keep nodes focused on a single responsibility
2. **Message Design**: Use appropriate message types and minimize message size
3. **Parameter Usage**: Use parameters for configuration, not for data
4. **Logging**: Use appropriate logging levels for debugging
5. **Shutdown Handling**: Properly handle node shutdown and resource cleanup
6. **Error Handling**: Implement robust error handling for real-world scenarios

## Sim-to-Real Transfer

The same ROS 2 concepts apply to both simulation and real robots. The main differences are:
- In simulation: Perfect sensing, no communication delays
- In reality: Sensor noise, communication delays, hardware failures
- Code structure remains the same, but robustness becomes more critical

This makes ROS 2 an excellent platform for sim-to-real transfer, as you can develop and test algorithms in simulation before deploying them to real hardware.