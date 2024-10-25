""" ARAP Webots main file """
import robot

def main():
    red = 0
    green = 0
    blue = 0
    range = 0.0
    robot1 = robot.ARAP()
    robot1.init_devices()
    
    while True:
        robot1.reset_actuator_values()
        range = robot1.get_sensor_input()
        robot1.blink_leds()
        red, green, blue = robot1.get_camera_image(5)
        
        print(red , green , blue)
        
        if robot1.front_obstacles_detected():
            robot1.move_backward()
            robot1.turn_left()
        else:
            robot1.run_braitenberg()
        robot1.set_actuators()
        robot1.step()

if __name__ == "__main__":
    main()