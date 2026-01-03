#!/usr/bin/env python3

"""
Basic ROS 2 Subscriber Example

This example demonstrates creating a simple subscriber node that listens
to messages on a topic and logs them.
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class MinimalSubscriber(Node):

    def __init__(self):
        super().__init__('minimal_subscriber')

        # Create a subscription to the 'topic' topic with String message type
        self.subscription = self.create_subscription(
            String,
            'topic',
            self.listener_callback,
            10)
        # Prevent unused variable warning
        self.subscription

    def listener_callback(self, msg):
        """Callback function that is called when a message is received"""
        self.get_logger().info('I heard: "%s"' % msg.data)


def main(args=None):
    """Main function to initialize and run the ROS 2 node"""
    rclpy.init(args=args)

    minimal_subscriber = MinimalSubscriber()

    try:
        # Spin the node so the callback function is called
        rclpy.spin(minimal_subscriber)
    except KeyboardInterrupt:
        pass
    finally:
        # Destroy the node explicitly
        minimal_subscriber.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()