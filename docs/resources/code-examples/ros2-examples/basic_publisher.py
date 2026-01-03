#!/usr/bin/env python3

"""
Basic ROS 2 Publisher Example

This example demonstrates creating a simple publisher node that sends
messages to a topic at a regular interval.
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('minimal_publisher')

        # Create a publisher on the 'topic' topic with String message type
        self.publisher_ = self.create_publisher(String, 'topic', 10)

        # Create a timer that calls the timer_callback method every 0.5 seconds
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)

        # Counter to keep track of published messages
        self.i = 0

    def timer_callback(self):
        """Callback function that publishes a message every timer tick"""
        msg = String()
        msg.data = 'Hello World: %d' % self.i
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.data)
        self.i += 1


def main(args=None):
    """Main function to initialize and run the ROS 2 node"""
    rclpy.init(args=args)

    minimal_publisher = MinimalPublisher()

    try:
        # Spin the node so the callback function is called
        rclpy.spin(minimal_publisher)
    except KeyboardInterrupt:
        pass
    finally:
        # Destroy the node explicitly
        minimal_publisher.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()