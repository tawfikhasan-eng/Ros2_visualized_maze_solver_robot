import math
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Pose, Twist
from std_msgs.msg import String


def fix_angle(a):
    if a > math.pi:
        fixed_angle = a - 2 * math.pi
    elif a < -math.pi:
        fixed_angle = a + 2 * math.pi
    else:
        fixed_angle = a
    return fixed_angle


class MazeController(Node):
    def __init__(self):
        super().__init__('maze_controller')

        self.left = 999.0
        self.front = 999.0
        self.right = 999.0

        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0

        self.have_sensors = False   
        self.have_pose = False    
        self.state = 'forward'     
        self.target = 0.0         

        self.last_x = None
        self.last_y = None
        open('pose.data', 'w').close()   

        self.pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.create_subscription(String, '/sensors_readings', self.on_sensors, 10)
        self.create_subscription(Pose, '/robot_pose', self.on_pose, 10)

        self.create_timer(0.05, self.loop)

    def on_sensors(self, msg):
        values = msg.data.split()
        self.left = float(values[0])
        self.front = float(values[1])
        self.right = float(values[2])
        self.have_sensors = True

    def on_pose(self, msg):
        self.x = msg.position.x
        self.y = msg.position.y
        self.theta = msg.orientation.z   

        if not self.have_pose:
            self.target = self.theta
            self.have_pose = True

        self.save_position()

    def save_position(self):
     
        if self.last_x is not None:
            distance = math.hypot(self.x - self.last_x, self.y - self.last_y)
            if distance < 0.02:
                return
        self.last_x = self.x
        self.last_y = self.y
        with open('pose.data', 'a') as f:        
            f.write(f"{{'x': {self.x:.3f}, 'y': {self.y:.3f}}}\n")

    def loop(self):
        if not (self.have_pose and self.have_sensors):
            return

        cmd = Twist()   

        if self.left >= 999 and self.front >= 999 and self.right >= 999:
            self.state = 'done'

        if self.state == 'forward':
            if self.front > 0.3:
                cmd.linear.x = 0.2         
            else:
                if self.right >= self.left:
                    self.target = self.target - math.pi / 2   
                else:
                    self.target = self.target + math.pi / 2   
                self.target = fix_angle(self.target)
                self.state = 'turn'

        elif self.state == 'turn':
            error = fix_angle(self.target - self.theta)  

            if abs(error) < 0.03:        
                self.state = 'forward'
            else:
                if abs(error) < 0.3:
                    speed = 0.15
                else:
                    speed = 0.5

                if error > 0:
                    cmd.angular.z = speed     
                else:
                    cmd.angular.z = -speed   


        self.pub.publish(cmd)


def main(args=None):
    rclpy.init(args=args)
    node = MazeController()
    rclpy.spin(node)
    rclpy.shutdown()
if __name__ == '__main__':
    main()

