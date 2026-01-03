#!/usr/bin/env python3

"""
Object Detection Example using OpenCV

This example demonstrates basic object detection using color-based segmentation
with OpenCV. It processes camera images to detect colored objects and publishes
their positions.
"""

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import String
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
            '/camera/image_raw',
            self.image_callback,
            10
        )

        # Create publisher for detected objects
        self.objects_pub = self.create_publisher(String, '/detected_objects', 10)

        # Initialize OpenCV bridge
        self.bridge = CvBridge()

        # Define color ranges in HSV space for detection
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
        """Process incoming camera image and detect objects"""
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


def main(args=None):
    """Main function to initialize and run the ROS 2 node"""
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