""" ARAP Webots main file """
import robot
import time


def counter( a , R , G , B):
    count = 0
    if a != count:
        count = a
        #print(a)                #Counter debug
        print(R , G , B)

        if R>200 and G<100 and B<100:
            print("Found Red")
        
        elif R<100 and G>150 and B<100:
            print("Found Green")
        
        elif R<100 and G<100 and B>150:
            print("Found Blue")


    else: 
        pass


def main():
    red = 0
    green = 0
    blue = 0
    range = 0.0
    past_duration = 0
    robot1 = robot.ARAP()
    robot1.init_devices()    
    
    
    start_time = time.time()
    while True: 
        
        end_time = time.time()
        duration = int(end_time - start_time)
        robot1.reset_actuator_values()
        
        range = robot1.get_sensor_input()
        robot1.blink_leds()
        red, green, blue = robot1.get_camera_image(5)


        if duration>past_duration:
            counter(duration , red, green, blue)
        past_duration = duration
        
        
        
        if robot1.front_obstacles_detected():
            robot1.move_backward()
            robot1.turn_left()
        else:
            robot1.run_braitenberg()
        robot1.set_actuators()
        robot1.step()

if __name__ == "__main__":
    main()