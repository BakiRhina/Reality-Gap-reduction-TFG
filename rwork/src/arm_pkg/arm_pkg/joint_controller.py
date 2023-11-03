import rclpy
import math

from rclpy.node import Node
from std_msgs.msg import Float64

class JointTorqueController(Node):
    def __init__(self):
        super().__init__('joint_torque_controller')
        
        self.joint_publishers = []
        self.joint_names = [
                            'joint0', 
                            'joint1', 
                            'joint2',
                            'joint3',
                            'joint4',
                            'right_finger_joint',
                            'left_finger_joint'
                            ]
        
        for joint_name in self.joint_names:
            publisher = self.create_publisher(Float64, f'/two_joint_arm/{joint_name}/pos_eff', 1)
            self.joint_publishers.append(publisher)

        self.timer = self.create_timer(1, self.move_joints)

        self.angle = 0

    def move_joints(self):

        # keep the angle between 0 and 2π
        self.angle = (self.angle + 10) % (2 * math.pi) 
        
        msg_joint0 = Float64()
        msg_joint1 = Float64()
        msg_joint2 = Float64()
        msg_joint3 = Float64()
        
        msg_joint0.data = 8.5 * math.sin(self.angle)# Apply a constant torque of x Nm
        msg_joint1.data = 9 * math.sin(self.angle)
        msg_joint2.data = 3 * math.sin(self.angle)
        msg_joint3.data = 1 * math.sin(self.angle)

        self.publisher_joint0.publish(msg_joint0)
        self.publisher_joint1.publish(msg_joint1)
        self.publisher_joint2.publish(msg_joint2)
        self.publisher_joint3.publish(msg_joint3)

        self.get_logger().info('Joint 0 torque: "%s"' % msg_joint0.data)
        self.get_logger().info('Joint 1 torque: "%s"' % msg_joint1.data)
        self.get_logger().info('Joint 2 torque: "%s"' % msg_joint2.data)
        self.get_logger().info('Joint 3 torque: "%s"' % msg_joint3.data)

def main(args=None):
    rclpy.init(args=args)
    joint_torque_controller = JointTorqueController()
    rclpy.spin(joint_torque_controller)
    joint_torque_controller.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
