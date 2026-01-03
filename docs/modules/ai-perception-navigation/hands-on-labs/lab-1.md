---
sidebar_label: 'Lab 1: Basic Object Detection'
sidebar_position: 1
---

# Lab 1: Basic Object Detection

In this lab, you'll implement basic object detection using computer vision techniques with ROS 2. You'll create a node that processes camera images to detect colored objects and publish their positions.

## Learning Objectives

After completing this lab, you will be able to:
- Process camera images using OpenCV in ROS 2
- Implement color-based object detection
- Use ROS 2 messages for perception data
- Integrate perception with other ROS 2 nodes

## Prerequisites

Before starting this lab, ensure you have:
- Completed the ROS 2 fundamentals and simulation modules
- OpenCV installed with Python bindings: `pip install opencv-python`
- Basic understanding of color spaces (RGB, HSV)
- Access to a simulated robot with camera (from previous modules)

## Step 1: Create the Perception Package

First, create a new ROS 2 package for perception nodes:

```bash
cd ~/ros2_labs/src
ros2 pkg create --build-type ament_python perception_tutorial
cd perception_tutorial
mkdir -p perception_tutorial
```

## Step 2: Create the Object Detection Node

Create the main object detection script at `perception_tutorial/object_detector.py`:

```python
#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import String
from geometry_msgs.msg import Point
from cv_bridge import CvBridge
import cv2
import numpy as np
import json


class ObjectDetector(Node):
    def __init__(self):
        super().__init__('object_detector')

        # Create subscriber for camera images
        self.image_sub = self.create_subscription(
            Image,
            '/simple_robot/camera/image_raw',
            self.image_callback,
            10
        )

        # Create publisher for detected objects
        self.objects_pub = self.create_publisher(String, '/detected_objects', 10)

        # Initialize OpenCV bridge
        self.bridge = CvBridge()

        # Define color ranges in HSV space
        # Format: (lower_hsv, upper_hsv, color_name)
        self.color_ranges = [
            ((0, 50, 50), (10, 255, 255), 'red'),
            ((100, 50, 50), (130, 255, 255), 'blue'),
            ((40, 50, 50), (80, 255, 255), 'green'),
            ((20, 50, 50), (40, 255, 255), 'yellow'),
        ]

        # Minimum area for detected objects (in pixels)
        self.min_area = 500

        self.get_logger().info('Object Detector initialized')

    def image_callback(self, msg):
        try:
            # Convert ROS image to OpenCV format
            cv_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")
        except Exception as e:
            self.get_logger().error(f'Could not convert image: {e}')
            return

        # Get image dimensions for relative positioning
        height, width = cv_image.shape[:2]

        # Store detected objects
        detected_objects = []

        # Process each color range
        for lower_hsv, upper_hsv, color_name in self.color_ranges:
            # Convert to HSV for better color detection
            hsv = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)

            # Create mask for current color range
            lower = np.array(lower_hsv)
            upper = np.array(upper_hsv)
            mask = cv2.inRange(hsv, lower, upper)

            # Apply morphological operations to reduce noise
            kernel = np.ones((5, 5), np.uint8)
            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
            mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

            # Find contours in the mask
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # Process each contour
            for contour in contours:
                area = cv2.contourArea(contour)
                if area > self.min_area:  # Filter small detections
                    # Calculate centroid
                    M = cv2.moments(contour)
                    if M["m00"] != 0:  # Avoid division by zero
                        cx = int(M["m10"] / M["m00"])
                        cy = int(M["m01"] / M["m00"])

                        # Calculate relative position (0-1)
                        rel_x = cx / width
                        rel_y = cy / height

                        # Calculate bounding box
                        x, y, w, h = cv2.boundingRect(contour)

                        # Calculate size as a percentage of image area
                        obj_size = (w * h) / (width * height) * 100

                        # Store object information
                        obj_info = {
                            'color': color_name,
                            'position': {'x': rel_x, 'y': rel_y},
                            'centroid': {'x': cx, 'y': cy},
                            'size': obj_size,
                            'area': area,
                            'bbox': {'x': x, 'y': y, 'width': w, 'height': h}
                        }

                        detected_objects.append(obj_info)

        # Publish detected objects as JSON string
        if detected_objects:
            objects_msg = String()
            objects_msg.data = json.dumps(detected_objects)
            self.objects_pub.publish(objects_msg)
            self.get_logger().info(f'Detected {len(detected_objects)} objects: {[obj["color"] for obj in detected_objects]}')
        else:
            # Publish empty result
            objects_msg = String()
            objects_msg.data = json.dumps([])
            self.objects_pub.publish(objects_msg)

    def visualize_detections(self, cv_image, detected_objects):
        """Optional: Draw detection results on image for visualization"""
        viz_image = cv_image.copy()

        for obj in detected_objects:
            bbox = obj['bbox']
            x, y, w, h = bbox['x'], bbox['y'], bbox['width'], bbox['height']
            color = obj['color']

            # Draw bounding box
            cv2.rectangle(viz_image, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Draw label
            label = f"{color}: {obj['size']:.1f}%"
            cv2.putText(viz_image, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            # Draw centroid
            cx, cy = obj['centroid']['x'], obj['centroid']['y']
            cv2.circle(viz_image, (cx, cy), 5, (0, 0, 255), -1)

        return viz_image


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

## Step 3: Create an Object Tracking Node

Create an additional node that tracks objects across frames at `perception_tutorial/object_tracker.py`:

```python
#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import Point
import json
import math


class ObjectTracker(Node):
    def __init__(self):
        super().__init__('object_tracker')

        # Create subscriber for detected objects
        self.objects_sub = self.create_subscription(
            String,
            '/detected_objects',
            self.objects_callback,
            10
        )

        # Create publisher for tracked objects
        self.tracked_pub = self.create_publisher(String, '/tracked_objects', 10)

        # Store tracked objects with history
        self.tracked_objects = {}  # ID -> object data
        self.next_id = 0

        # Parameters for tracking
        self.max_distance = 0.1  # Maximum distance for association (relative coordinates)
        self.history_length = 10  # Number of positions to remember
        self.min_observations = 3  # Minimum observations to consider valid

        self.get_logger().info('Object Tracker initialized')

    def objects_callback(self, msg):
        try:
            detected_objects = json.loads(msg.data)
        except json.JSONDecodeError:
            self.get_logger().error('Could not parse detected objects JSON')
            return

        # Update tracked objects based on new detections
        new_tracked = {}
        used_detections = set()

        # Associate new detections with existing tracks
        for detected_obj in detected_objects:
            best_match_id = None
            best_distance = float('inf')

            for track_id, track_data in self.tracked_objects.items():
                if track_id in new_tracked:  # Already matched
                    continue

                # Calculate distance between detected object and existing track
                detected_pos = detected_obj['position']
                track_pos = track_data['positions'][-1]  # Last known position

                distance = math.sqrt(
                    (detected_pos['x'] - track_pos['x'])**2 +
                    (detected_pos['y'] - track_pos['y'])**2
                )

                if distance < self.max_distance and distance < best_distance:
                    best_distance = distance
                    best_match_id = track_id

            if best_match_id is not None:
                # Update existing track
                track_data = self.tracked_objects[best_match_id]
                track_data['positions'].append(detected_obj['position'])
                track_data['positions'] = track_data['positions'][-self.history_length:]  # Keep only recent positions
                track_data['last_seen'] = self.get_clock().now().nanoseconds
                track_data['current_data'] = detected_obj
                new_tracked[best_match_id] = track_data
                used_detections.add(detected_objects.index(detected_obj))
            else:
                # Create new track
                new_id = self.next_id
                self.next_id += 1
                new_tracked[new_id] = {
                    'id': new_id,
                    'color': detected_obj['color'],
                    'positions': [detected_obj['position']],
                    'current_data': detected_obj,
                    'first_seen': self.get_clock().now().nanoseconds,
                    'last_seen': self.get_clock().now().nanoseconds,
                    'observations': 1
                }

        # Add unassociated detections as new tracks
        for i, detected_obj in enumerate(detected_objects):
            if i not in used_detections:
                new_id = self.next_id
                self.next_id += 1
                new_tracked[new_id] = {
                    'id': new_id,
                    'color': detected_obj['color'],
                    'positions': [detected_obj['position']],
                    'current_data': detected_obj,
                    'first_seen': self.get_clock().now().nanoseconds,
                    'last_seen': self.get_clock().now().nanoseconds,
                    'observations': 1
                }

        # Update existing tracks that weren't matched (predict position)
        for track_id, track_data in self.tracked_objects.items():
            if track_id not in new_tracked:
                # Object not detected, but we might still want to keep tracking for a short time
                time_since_seen = (self.get_clock().now().nanoseconds - track_data['last_seen']) / 1e9
                if time_since_seen < 0.5:  # Keep for 0.5 seconds
                    new_tracked[track_id] = track_data

        # Update tracked objects
        self.tracked_objects = new_tracked

        # Filter out tracks with insufficient observations and publish
        valid_tracks = [
            track_data for track_data in self.tracked_objects.values()
            if track_data['observations'] >= self.min_observations
        ]

        if valid_tracks:
            tracked_msg = String()
            tracked_msg.data = json.dumps(valid_tracks)
            self.tracked_pub.publish(tracked_msg)

        self.get_logger().info(f'Tracking {len(valid_tracks)} objects')


def main(args=None):
    rclpy.init(args=args)

    tracker = ObjectTracker()

    try:
        rclpy.spin(tracker)
    except KeyboardInterrupt:
        pass
    finally:
        tracker.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
```

## Step 4: Create a Launch File

Create a launch file to start both nodes at `launch/object_detection.launch.py`:

```python
from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    # Object detection node
    object_detector = Node(
        package='perception_tutorial',
        executable='object_detector',
        name='object_detector',
        output='screen',
        parameters=[
            # Add parameters here if needed
        ]
    )

    # Object tracking node
    object_tracker = Node(
        package='perception_tutorial',
        executable='object_tracker',
        name='object_tracker',
        output='screen',
        parameters=[
            # Add parameters here if needed
        ]
    )

    ld = LaunchDescription()
    ld.add_action(object_detector)
    ld.add_action(object_tracker)

    return ld
```

## Step 5: Update Setup.py

Update the `setup.py` file to include the new executables:

```python
from setuptools import find_packages, setup

package_name = 'perception_tutorial'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', ['launch/object_detection.launch.py']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Your Name',
    maintainer_email='your.email@example.com',
    description='Basic object detection tutorial',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'object_detector = perception_tutorial.object_detector:main',
            'object_tracker = perception_tutorial.object_tracker:main',
        ],
    },
)
```

## Step 6: Install Dependencies

Install required dependencies:

```bash
pip install opencv-python cv-bridge numpy
```

## Step 7: Build the Package

Build the perception package:

```bash
cd ~/ros2_labs
source /opt/ros/humble/setup.bash
colcon build --packages-select perception_tutorial
source install/setup.bash
```

## Step 8: Run the Object Detection System

First, start the simulation environment from a previous lab:

```bash
# Terminal 1: Start the simulation (from robot_sim_description package)
cd ~/ros2_labs
source install/setup.bash
ros2 launch robot_sim_description robot_sim.launch.py
```

Then in a new terminal, run the object detection system:

```bash
# Terminal 2: Start the object detection nodes
cd ~/ros2_labs
source install/setup.bash
ros2 launch perception_tutorial object_detection.launch.py
```

## Step 9: Visualize the Results

In a third terminal, monitor the detection results:

```bash
# Terminal 3: Monitor detected objects
cd ~/ros2_labs
source install/setup.bash
ros2 topic echo /detected_objects

# Or monitor tracked objects
ros2 topic echo /tracked_objects
```

## Step 10: Test with Different Objects

You can add colored objects to your simulation environment or modify the colors in the simulation to test detection:

```bash
# In Gazebo, you can add colored boxes or modify your robot model
# Or send test images if you're using a camera feed
```

## Step 11: Create a Simple Test Node

Create a simple node to test the system at `perception_tutorial/test_perception.py`:

```python
#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import json


class PerceptionTester(Node):
    def __init__(self):
        super().__init__('perception_tester')

        # Subscribe to tracked objects
        self.tracked_sub = self.create_subscription(
            String,
            '/tracked_objects',
            self.tracked_callback,
            10
        )

        self.get_logger().info('Perception Tester initialized')

    def tracked_callback(self, msg):
        try:
            tracked_objects = json.loads(msg.data)
        except json.JSONDecodeError:
            self.get_logger().error('Could not parse tracked objects JSON')
            return

        if tracked_objects:
            self.get_logger().info(f'Found {len(tracked_objects)} tracked objects:')
            for obj in tracked_objects:
                pos = obj['current_data']['position']
                self.get_logger().info(f'  Object ID {obj["id"]} ({obj["color"]}) at position ({pos["x"]:.2f}, {pos["y"]:.2f})')
        else:
            self.get_logger().info('No objects currently tracked')


def main(args=None):
    rclpy.init(args=args)

    tester = PerceptionTester()

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
        'object_detector = perception_tutorial.object_detector:main',
        'object_tracker = perception_tutorial.object_tracker:main',
        'test_perception = perception_tutorial.test_perception:main',
    ],
},
```

## Step 12: Rebuild and Test

```bash
cd ~/ros2_labs
source /opt/ros/humble/setup.bash
colcon build --packages-select perception_tutorial
source install/setup.bash

# Run the complete system
# Terminal 1: Simulation
ros2 launch robot_sim_description robot_sim.launch.py

# Terminal 2: Perception nodes
ros2 launch perception_tutorial object_detection.launch.py

# Terminal 3: Test node
ros2 run perception_tutorial test_perception
```

## Expected Results

- The object detector should identify colored objects in the camera feed
- The tracker should maintain consistent IDs for objects across frames
- The test node should report the positions of tracked objects
- You should see detection and tracking information in the console

## Troubleshooting

### Common Issues

**Issue**: "Could not convert image: cv_bridge error"
**Solution**: Check the image encoding format in Gazebo and make sure it's compatible with cv_bridge

**Issue**: No objects detected
**Solution**:
- Verify the simulation is running and camera is publishing images
- Check color ranges in HSV space
- Adjust `min_area` parameter for smaller/larger objects

**Issue**: Dependencies not found
**Solution**:
```bash
pip install opencv-python cv-bridge numpy
```

**Issue**: Nodes not communicating
**Solution**: Verify topic names match between publisher and subscriber

## Understanding the Implementation

### Object Detection Approach
- Color-based detection in HSV space (more robust than RGB)
- Morphological operations to reduce noise
- Contour analysis to find object shapes
- Centroid calculation for position estimation

### Object Tracking Approach
- Association based on position proximity
- History maintenance for trajectory estimation
- Temporal consistency to maintain tracks

### ROS 2 Integration
- Proper message types for image and perception data
- Efficient image transport using cv_bridge
- JSON serialization for complex object data

## Extensions

To extend this basic implementation:

1. **Add Shape Detection**: Use contour analysis to detect specific shapes
2. **Implement Depth Perception**: Use stereo cameras or depth sensors
3. **Add Machine Learning**: Integrate deep learning models for object classification
4. **Improve Tracking**: Use more sophisticated tracking algorithms like Kalman filters

## Assessment

To verify you've completed this lab successfully:
1. You can detect colored objects in the camera feed
2. The tracker maintains consistent IDs across frames
3. You can monitor the detection and tracking results
4. The system processes images in real-time

## Sim-to-Real Connection

The same principles used in this simulation will apply to real robots:
- Color-based detection works with real cameras
- Tracking algorithms remain the same
- The main differences will be in lighting conditions and sensor quality

Congratulations! You've implemented a basic perception system that detects and tracks colored objects using ROS 2.