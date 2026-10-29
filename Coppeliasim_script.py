class PioneerRobot:
    def __init__(self):
        global no_echo
        no_echo = 999
        self.leftMotor = sim.getObject('../leftMotor')
        self.rightMotor = sim.getObject('../rightMotor')
        self.pioneer = sim.getObject('..')

        self.left_sensor = sim.getObject('../visible/ultrasonicSensor[0]')
        self.front_sensor = sim.getObject('../visible/ultrasonicSensor[3]')
        self.right_sensor = sim.getObject('../visible/ultrasonicSensor[7]')

        self.sensors = [self.left_sensor, self.front_sensor, self.right_sensor]

        self.robot = sim.getObject('..')
        
        self.readings = [no_echo, no_echo, no_echo]

        self.linear = 0.0
        self.angular = 0.0

        self.pub_sensors = simROS2.createPublisher(
            '/sensors_readings', 'std_msgs/msg/String')
        self.pub_pose = simROS2.createPublisher(
            '/robot_pose', 'geometry_msgs/msg/Pose')
        self.sub_cmd = simROS2.createSubscription(
            '/cmd_vel', 'geometry_msgs/msg/Twist', 'velocity')

    def read_sensors(self):
        values = []
        for i in range(3):
            result, distance, _ , _ , _ = sim.readProximitySensor(self.sensors[i])
            if result:
                values.append(round(distance, 3))
            else:
                values.append(no_echo)
        self.readings = values

    def move(self, v, w):
        car_width = 0.33
        left = v - (w * car_width / 2.0)
        right = v + (w * car_width / 2.0)
        sim.setJointTargetVelocity(self.leftMotor, left*10)
        sim.setJointTargetVelocity(self.rightMotor, right*10)


def velocity(msg):
    robot.linear = msg['linear']['x']
    robot.angular = msg['angular']['z']


def sysCall_init():
    global sim, simROS2, robot
    sim = require('sim')
    simROS2 = require('simROS2')
    robot = PioneerRobot()


def sysCall_actuation():
    robot.move(robot.linear, robot.angular)


def sysCall_sensing():
    robot.read_sensors()
    left, front, right = robot.readings

    x, y, z = sim.getObjectPosition(robot.pioneer, sim.handle_world)
    qx, qy, qz = sim.getObjectOrientation(robot.pioneer, sim.handle_world)
    
    msg_sensors = {
        'data': f'{left} {front} {right}'
    }
    msg_pose = {
        'position': {
            'x': x,
            'y': y, 
            'z': z
        },
        'orientation': {
            'x': qx, 
            'y': qy, 
            'z': qz,
            'w': 0.0
        },
    }
    simROS2.publish(robot.pub_sensors, msg_sensors)
    simROS2.publish(robot.pub_pose, msg_pose)
    


def sysCall_cleanup():

    pass

