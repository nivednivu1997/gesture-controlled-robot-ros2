import rclpy
from rclpy.node import Node
import serial
import threading
import time

from geometry_msgs.msg import Twist


class SerialIMUReader(Node):
    def __init__(self):
        super().__init__('serial_imu_reader')
        self.declare_parameter('serial_port', '/dev/ttyUSB0')
        self.declare_parameter('baud_rate', 115200)

        serial_port = self.get_parameter('serial_port').get_parameter_value().string_value
        baud_rate = self.get_parameter('baud_rate').get_parameter_value().integer_value

        # Publisher for cmd_vel
        self.cmd_vel_pub = self.create_publisher(Twist, '/model/tugbot/cmd_vel', 10)

        try:
            self.ser = serial.Serial(serial_port, baud_rate, timeout=1)
            self.get_logger().info(f'Connected to {serial_port} at {baud_rate} baud')
            time.sleep(2)  # Let the device reset
            self.running = True
            self.thread = threading.Thread(target=self.read_serial_loop)
            self.thread.start()
        except serial.SerialException as e:
            self.get_logger().error(f"Failed to connect to {serial_port}: {e}")
            self.ser = None

    def read_serial_loop(self):
        while self.running and self.ser:
            try:
                line = self.ser.readline().decode('utf-8', errors='ignore').strip()
                if line.startswith("ypr"):
                    parts = line.split('\t')
                    if len(parts) == 4:
                        yaw = float(parts[1])
                        pitch = float(parts[2])
                        roll = float(parts[3])
                        self.get_logger().info(f"Yaw: {yaw:.2f}, Pitch: {pitch:.2f}, Roll: {roll:.2f}")
                        self.publish_cmd_vel(yaw, pitch)
            except Exception as e:
                self.get_logger().warn(f"Serial read failed: {e}")

    def publish_cmd_vel(self, yaw, pitch):
        twist = Twist()

        # Forward / Backward motion based on pitch
        if pitch < -50:
            twist.linear.x = -0.2  # Move forward
        elif pitch > 50:
            twist.linear.x = 0.2  # Move backward

        # Left / Right rotation based on yaw
        if yaw < -50:
            twist.angular.z = 0.5  # Turn left
        elif yaw > 50:
            twist.angular.z = -0.5  # Turn right

        self.cmd_vel_pub.publish(twist)

    def destroy_node(self):
        self.running = False
        if self.thread.is_alive():
            self.thread.join()
        if self.ser:
            self.ser.close()
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = SerialIMUReader()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Shutting down node.")
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
