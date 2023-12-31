import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from geometry_msgs.msg import PoseArray

class robotState(Node):
    def __init__(self):
        super().__init__('robot_state')

        self.get_logger().info('Starting Node')

        self.grippers_subscription = self.create_subscription(
            PoseArray,
            '/world/full_env/dynamic_pose/info',
            self.gripper_pose,
            1)

        self.j1_subscription = self.create_subscription(
            JointState,
            '/world/full_env/model/arm_1/joint_state',
            self.joint_angles_1,
            1)
        
        self.j2_subscription = self.create_subscription(
            JointState,
            '/world/full_env/model/arm_2/joint_state',
            self.joint_angles_2,
            1)

        

        ######  GRIPPER GENERAL COORDENATES FUNCTIONS ######
    
    def extract_coordinates(self, pose):
        
        return {
            "x": pose.position.x,
            "y": pose.position.y,
            "z": pose.position.z,
            "orientation": {
                "x": pose.orientation.x,
                "y": pose.orientation.y,
                "z": pose.orientation.z,
                "w": pose.orientation.w
            }
        }

    def gripper_pose(self, msg: PoseArray):

        ef_rb1 = msg.poses[15]
        ef_rb2 = msg.poses[27]

        ef1_data = self.extract_coordinates(ef_rb1)
        ef2_data = self.extract_coordinates(ef_rb2)

        self.get_logger().info(
            f'Pose gripper 1: {ef1_data}'
            )
        self.get_logger().info(
            f'Pose gripper 2: {ef2_data}'
            )
        
                ######  JOINT ANGLES FUNCTIONS ######

    def joint_angles_1(self, msg):
        self.get_logger().info('Joints 1')
        for name, position in zip(msg.name, msg.position):
            self.get_logger().info(f'Joint: {name}, Angle: {position}')
    
    def joint_angles_2(self, msg):
        self.get_logger().info('Joints 2')
        for name, position in zip(msg.name, msg.position):
            self.get_logger().info(f'Joint: {name}, Angle: {position}')



                 ######  INITIALIZATION FUNCTIONS ######


def main(args=None):
    rclpy.init(args=args)
    robot_state = robotState()
    rclpy.spin(robot_state)
    robot_state.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
