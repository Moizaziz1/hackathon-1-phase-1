---
sidebar_label: 'Resources'
sidebar_position: 3
---

# ROS 2 Resources

This page contains additional resources to support your learning of ROS 2 fundamentals.

## Official Documentation

- [ROS 2 Documentation](https://docs.ros.org/en/humble/) - The official ROS 2 documentation for Humble Hawksbill
- [ROS 2 Tutorials](https://docs.ros.org/en/humble/Tutorials.html) - Step-by-step tutorials for ROS 2
- [ROS 2 Concepts](https://docs.ros.org/en/humble/Concepts.html) - In-depth explanations of ROS 2 concepts

## Essential Packages

### Core Packages
- `rclpy`: Python client library for ROS 2
- `rclcpp`: C++ client library for ROS 2
- `std_msgs`: Standard message types
- `sensor_msgs`: Message types for sensors
- `geometry_msgs`: Message types for geometry
- `nav_msgs`: Message types for navigation
- `tf2`: Transform library for coordinate frames

### Development Tools
- `rqt`: Qt-based framework for GUI development
- `rviz2`: 3D visualization tool
- `ros2cli`: Command-line tools for ROS 2

## Code Examples

### Python Examples
- Basic Publisher/Subscriber: `demo_nodes_py`
- Services: `demo_nodes_py`
- Actions: `demo_nodes_py`
- Parameters: `demo_nodes_py`

### C++ Examples
- Basic Publisher/Subscriber: `demo_nodes_cpp`
- Services: `demo_nodes_cpp`
- Actions: `demo_nodes_cpp`

## Simulation Environments

### Gazebo
- [Gazebo Classic](http://classic.gazebosim.org/)
- [Ignition Gazebo](https://ignitionrobotics.org/)
- [Gazebo ROS2 Bridge](https://github.com/ros-simulation/gazebo_ros_pkgs)

### Webots
- [Webots Simulator](https://cyberbotics.com/)
- [Webots ROS2 Interface](https://github.com/cyberbotics/webots_ros2)

### Isaac Sim
- [NVIDIA Isaac Sim](https://developer.nvidia.com/isaac-sim)
- [Isaac ROS](https://github.com/NVIDIA-ISAAC-ROS)

## ROS 2 Distributions

- **Humble Hawksbill (LTS)**: Current Long Term Support release (recommended)
- **Iron Irwini**: Latest release
- **Rolling Ridley**: Development release (not recommended for beginners)

## Development Best Practices

### Code Organization
```
package_name/
├── CMakeLists.txt
├── package.xml
├── src/
│   └── node_name.cpp
├── include/
│   └── package_name/
│       └── node_name.hpp
├── launch/
│   └── launch_file.launch.py
├── config/
│   └── parameters.yaml
└── test/
    └── test_file.cpp
```

### Naming Conventions
- Package names: lowercase with underscores
- Node names: lowercase with underscores
- Topic names: lowercase with forward slashes
- Parameter names: lowercase with underscores

### Performance Considerations
- Use appropriate QoS settings for your use case
- Minimize message size for high-frequency topics
- Use latching for static transforms
- Consider using intra-process communication for performance-critical nodes

## Troubleshooting Common Issues

### Network Configuration
- Ensure ROS_DOMAIN_ID is set consistently across machines
- Check network connectivity between ROS 2 nodes
- Use `ros2 topic list` to verify communication

### Performance Issues
- Monitor CPU and memory usage
- Use appropriate timer rates
- Consider using multithreading for I/O operations

### Debugging Tips
- Use `ros2 topic echo` to inspect messages
- Use `ros2 node info` to check node connections
- Use logging for debugging: `self.get_logger().info()`

## Community Resources

- [ROS Answers](https://answers.ros.org/) - Q&A forum for ROS questions
- [ROS Discourse](https://discourse.ros.org/) - Community discussion forum
- [ROS Wiki](http://wiki.ros.org/) - Community-maintained documentation
- [ROS Robotics Stack Exchange](https://robotics.stackexchange.com/) - Robotics-focused Q&A

## Related Technologies

### Build Systems
- `ament_cmake`: CMake-based build system for ROS 2
- `colcon`: Multi-package build system

### Version Control
- Git workflows for ROS 2 packages
- Repository organization best practices

### Deployment
- Docker containers for ROS 2 applications
- Cross-compilation for embedded systems
- Real-time considerations for critical applications

## Learning Path

1. Start with official ROS 2 tutorials
2. Practice with the hands-on labs in this module
3. Explore simulation environments
4. Progress to more advanced concepts like navigation and perception
5. Apply knowledge to the capstone project

Remember to always follow the principles of "Accuracy First" and "Technical Excellence" when implementing ROS 2 code, ensuring your implementations are both correct and maintainable.