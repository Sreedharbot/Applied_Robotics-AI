""" ARAP Webots Standard Controller """
from controller import Robot, Motor, LED, DistanceSensor, Camera
import sys

class ARAP:
    # Robot constants
    MOTORS_NUMBER = 2
    DISTANCE_SENSORS_NUMBER = 8
    #GROUND_SENSORS_NUMBER = 3
    LEDS_NUMBER = 10
    LEFT = 0
    RIGHT = 1
    LED_ON = 255
    LED_OFF = 0
    MAX_SPEED = 6.28
    DELAY = 0.5
    MULTIPLIER = 0.5
    OBSTACLE_DISTANCE = 0.02
    
    motor_names = ("left wheel motor", "right wheel motor")
    distance_sensors_names = ("ps0", "ps1", "ps2", "ps3", "ps4", "ps5", "ps6", "ps7")
    #ground_sensors_names = ("gs0", "gs1", "gs2")
    leds_names = ("led0", "led1", "led2", "led3", "led4", "led5", "led6", "led7", "led8", "led9")
    camera_names = "camera"
    
    # Braitenberg constants
    weights = [ [-1.3, -1.0], 
                [-1.3, -1.0], 
                [-0.5, 0.5], 
                [0.0, 0.0], 
                [0.0, 0.0], 
                [0.05, -0.5], 
                [-0.75, 0.0], 
                [-0.75, 0.0] ]
    
    lookup_table = [ [0.0, 4095.0, 0.002], 
                 [0.005, 2133.33, 0.003], 
                 [0.01, 1465.73, 0.007], 
                 [0.015, 601.46, 0.0406], 
                 [0.02, 383.84, 0.01472], 
                 [0.03, 234.93, 0.0241], 
                 [0.04, 158.03, 0.0287], 
                 [0.05, 120.0, 0.04225], 
                 [0.06, 104.09, 0.03065], 
                 [0.07, 67.19, 0.04897] ]
    
    offsets = [MULTIPLIER * MAX_SPEED, MULTIPLIER * MAX_SPEED]
    
    def __init__(self):
        # Robot instance
        self.robot = Robot()
        self.time_step = int(self.robot.getBasicTimeStep())
        
        # Robot instance attributes
        self.distance_sensors = []
        self.distance_sensors_values = []
        self.distance_range = 0.0
        #self.ground_sensors = []
        #self.ground_sensors_values = [0.0, 0.0, 0.0]
        self.leds = []
        self.leds_values = []  # values: 0 - 255
        self.speeds = [0.0, 0.0]
        self.camera = None
        self.left_motor = None
        self.right_motor = None
        
        # Support attributes
        self.counter = 0
        self.camera_interval = 0
        self.red = 0
        self.green = 0
        self.blue = 0
        
        # Run init methods
        self.init_devices()

    def init_devices(self):
        # Distance sensors initialisation
        for i in range(self.DISTANCE_SENSORS_NUMBER):
            self.distance_sensors.append(self.robot.getDevice(self.distance_sensors_names[i]))
            self.distance_sensors_values.append(0.0)
            self.distance_sensors[i].enable(self.time_step)
            
        # Ground sensors initialisation
        #for i in range(self.GROUND_SENSORS_NUMBER):
        #    self.ground_sensors.append(self.robot.getDevice(self.ground_sensors_names[i]))
        #    self.ground_sensors_values.append(0.0)
        #    self.ground_sensors[i].enable(self.time_step)
            
        # LEDs initialisation
        for i in range(self.LEDS_NUMBER):
            self.leds.append(self.robot.getDevice(self.leds_names[i]))
            self.leds_values.append(self.LED_OFF)
            if self.leds[i].get() > self.LED_OFF:
                self.leds[i].set(self.LED_OFF)
            
        # Camera initialisation
        self.camera = self.robot.getDevice(self.camera_names)
        self.camera.enable(self.time_step)
        
        # Motors initialisation
        self.left_motor = self.robot.getDevice(self.motor_names[self.LEFT])
        self.right_motor = self.robot.getDevice(self.motor_names[self.RIGHT])
        self.left_motor.setPosition(float('inf'))
        self.right_motor.setPosition(float('inf'))
        self.left_motor.setVelocity(self.MAX_SPEED * 0.0)
        self.right_motor.setVelocity(self.MAX_SPEED * 0.0)
        
        self.step()
        
    def wait(self, sec):
        start_time = self.robot.getTime()
        elapsed_time = start_time
        while start_time + sec > self.robot.getTime():
            self.step()
        return True
            
    def reset_actuator_values(self):
        for i in range(2):
            self.speeds[i] = 0.0
        
        for i in range(self.LEDS_NUMBER):
            self.leds_values[i] = self.LED_OFF
            
        for i in range(self.DISTANCE_SENSORS_NUMBER):
            self.distance_sensors_values[i] = 0.0

    def set_actuators(self):
        for i in range(self.LEDS_NUMBER):
            self.leds[i].set(self.leds_values[i])
        self.left_motor.setVelocity(self.speeds[self.LEFT])
        self.right_motor.setVelocity(self.speeds[self.RIGHT])

    def blink_leds(self):
        brightness = int(((self.counter / 10) % self.LEDS_NUMBER) * 255)
        if brightness > self.LED_ON:
            self.counter = 0
        
        for i in range(self.LEDS_NUMBER):
            self.leds_values[i] = brightness
            #print("LED[", i, "] =", self.leds_values[i])  # DEBUG
        self.counter += 1

    def get_sensor_input(self):
        for i in range(self.DISTANCE_SENSORS_NUMBER):
            self.distance_sensors_values[i] = self.distance_sensors[i].getValue()
            sensor_total = self.distance_sensors_values[0] + self.distance_sensors_values[7]  # get front distance range from ps0 and ps7
            
            # Translate sensor_total value to lookup_table values
            for j in range(len(self.lookup_table)):
                if sensor_total >= self.lookup_table[j][1]:
                    self.distance_range = self.lookup_table[j][0]
                    break
            #print(self.distance_range)  # DEBUG
            
            # Normalise distance sensor values between 0.0 and 1.0
            self.distance_sensors_values[i] /= 4096;  # 1.0 = avoid, 0.0 = no avoid
            if self.distance_sensors_values[i] > 1.0:
                self.distance_sensors_values[i] = 1.0  # truncate max value to 1.0
            #print("Sensor[", i, "] =", self.distance_sensors_values[i])  # DEBUG
        return self.distance_range

    def get_time_step(self):
        self.time_step = -1
        if self.time_step == -1:
            self.time_step = int(self.robot.getBasicTimeStep())
        return self.time_step
    
    def step(self):
        if self.robot.step(self.get_time_step()) == -1:
            sys.exit(0)
    
    def get_camera_image(self, interval):
        width = self.camera.getWidth()
        height = self.camera.getHeight()
        image = self.camera.getImage()
        
        # Capture new image after interval (no. of steps) has passed
        if self.camera_interval >= interval:
            for x in range(width):
                for y in range(height):
                    self.red += self.camera.imageGetRed(image, self.camera.getWidth(), x, y)
                    self.green += self.camera.imageGetGreen(image, self.camera.getWidth(), x, y)
                    self.blue += self.camera.imageGetBlue(image, self.camera.getWidth(), x, y)
            self.red = int(self.red / (width * height))  # normalise wrt image size
            self.green = int(self.green / (width * height))  # normalise wrt image size
            self.blue = int(self.blue / (width * height))  # normalise wrt image size
            self.camera_interval = 0
        else:
            self.red = 0
            self.green = 0
            self.blue = 0
            self.camera_interval += 1
        
        #print("Camera: R =", self.red, ", G =", self.green, ", B =", self.blue)  # DEBUG
        return self.red, self.green, self.blue
    
    #def ground_obstacles_detected(self):
    #    for i in range(self.GROUND_SENSORS_NUMBER):
    #        if not self.ground_sensors[i]:
    #            return False
    #        if self.ground_sensors_values[i] < 500.0:
    #            return True
    #    else:
    #        return False
    
    def front_obstacles_detected(self):
        average = ( self.distance_sensors_values[0] + self.distance_sensors_values[7] ) / 2.0
        #print("Front sensor:", average)  # DEBUG
        if average > self.OBSTACLE_DISTANCE:
            return True
        else:
            return False
        
    def back_obstacles_detected(self):
        average = ( self.distance_sensors_values[3] + self.distance_sensors_values[4] ) / 2.0
        #print("Back sensor:", average)  # DEBUG
        if average > self.OBSTACLE_DISTANCE:
            return True
        else:
            return False
        
    def left_obstacles_detected(self):
        average = ( self.distance_sensors_values[5] + self.distance_sensors_values[6] ) / 2.0
        #print("Left sensor:", average)  # DEBUG
        if average > self.OBSTACLE_DISTANCE:
            return True
        else:
            return False
        
    def right_obstacles_detected(self):
        average = ( self.distance_sensors_values[1] + self.distance_sensors_values[2] ) / 2.0
        #print("Right sensor:", average)  # DEBUG
        if average > self.OBSTACLE_DISTANCE:
            return True
        else:
            return False
    
    def run_braitenberg(self):
        for i in range(2):
            self.speeds[i] = 0.0
            
            for j in range(self.DISTANCE_SENSORS_NUMBER):
                self.speeds[i] += self.distance_sensors_values[j] * self.weights[j][i]
            
            self.speeds[i] = self.offsets[i] + self.speeds[i] * self.MAX_SPEED
            if self.speeds[i] > self.MAX_SPEED:
                self.speeds[i] = self.MAX_SPEED
            elif self.speeds[i] < -self.MAX_SPEED:
                self.speeds[i] = -self.MAX_SPEED
        #print("Speeds: left =", self.speeds[self.LEFT], ", right =", self.speeds[self.RIGHT])  # DEBUG

    def move(self, left_multiplier, right_multiplier):
        # Left and Right multiplier values must be between 0.0 to -/+1.0
        self.left_motor.setVelocity(left_multiplier * self.MAX_SPEED)
        self.right_motor.setVelocity(right_multiplier * self.MAX_SPEED)
        self.wait(self.DELAY)

    def move_forward(self):
        self.left_motor.setVelocity(self.MAX_SPEED * self.MULTIPLIER)
        self.right_motor.setVelocity(self.MAX_SPEED * self.MULTIPLIER)
        self.wait(self.DELAY)
        
    def move_backward(self):
        self.left_motor.setVelocity(-self.MAX_SPEED * self.MULTIPLIER)
        self.right_motor.setVelocity(-self.MAX_SPEED * self.MULTIPLIER)
        self.wait(self.DELAY)

    def turn_left(self):
        self.left_motor.setVelocity(-self.MAX_SPEED * self.MULTIPLIER)
        self.right_motor.setVelocity(self.MAX_SPEED * self.MULTIPLIER)
        self.wait(self.DELAY)
    
    def turn_right(self):
        self.left_motor.setVelocity(self.MAX_SPEED * self.MULTIPLIER)
        self.right_motor.setVelocity(-self.MAX_SPEED * self.MULTIPLIER)
        self.wait(self.DELAY)
