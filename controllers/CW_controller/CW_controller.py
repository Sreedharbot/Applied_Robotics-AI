""" ARAP Webots main file """
import robot
import time





def counter( a ):
    count = 0
    if a != count:
        count = a
        #print(a)                #Counter debug
        
    else: 
        pass

def Red_OBS():
    return 1
        

def Green_OBS():
    return 2

        
def Blue_OBS():
    return 3



def main():
    red = 0
    green = 0
    blue = 0
    
    c = 0
    a = True
    value = 0
    count_box = 0 

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


        if duration > past_duration:
            counter(duration)
        past_duration = duration
        #print(status)                                        #debug the status Condition 

    


        if (red>=200) and (green<100) and (blue<100):
            b = Red_OBS()
            if b == 1 and a == True:
                count_box = count_box + 1
                print("Found RED Box - ", a , " " , count_box)
                value = 1
                a = False


        elif(red<100) and (green>=200) and (blue<100):
            b = Green_OBS()
            if b == 2 and a == True:
                count_box = count_box + 1
                print("Found GREEN Box - ", a ," ", count_box)
                value = 2
                a = False
            
        
        elif(red<100) and (green<100) and (blue>=150):
            b = Blue_OBS()
            if b == 3 and a == True:
                count_box = count_box + 1
                print("Found BLUE Box - ", a ," ", count_box)
                value = 3
                a = False
    
        
        else:
            if a == False and b == 0:
                c = c + 1
                #print(c)                    #Counter to clear the status 
                b = 1
                if c>40:
                    a = True
                    c=0
            else:
                b = 0

        if robot1.front_obstacles_detected():
            robot1.move_backward()
            robot1.turn_left()
        else:
            robot1.run_braitenberg()
        robot1.set_actuators()
        robot1.step()

if __name__ == "__main__":
    main()
    
    
