""" ARAP Webots main file """
import robot
import time
import cv2 as cv
import numpy as np






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


def pervious_box(a , b , k):
    
    old_value = k
    current_value = a
    
    #print (" before loop  old - ", old_value ," current - ",current_value, " b - status - ", b)                 #debugging conditions before entering the if-condition

    
    if (old_value == 1) and (current_value > old_value) and (b == True):
        print("Pervious box : RED")
        b = False

    elif (old_value == 1) and (current_value == old_value) and (b == True):
        print("Pervious box : RED")
        b = False
    
    elif (old_value == 2) and (current_value < old_value)  and (b == True):
        print("Pervious box : GREEN")
        b = False

    elif (old_value == 2) and (current_value > old_value)  and (b == True):
        print("Pervious box : GREEN")
        b = False
    
    elif (old_value == 2) and (current_value == old_value) and (b == True):
        print("Pervious box : GREEN")
        b = False
    
    elif (old_value == 3) and (current_value < old_value) and (b == True):
        print("Pervious box : BLUE")
        b = False
    
    elif (old_value == 3) and (current_value == old_value) and (b == True):
        print("Pervious box : BLUE")
        b = False

    old_value  =  current_value
    
    #print (" After  loop  old - ", old_value ," current - ",current_value, " b - status - ", b)                   #debugging conditions before entering the if-condition
    
    return old_value

def extracting_data_image(image,width,height,intervel):
    w = width
    h = height
    if intervel >= 5:
        for i in range(width):
            for j in range (height):
                value = image[width,height]
        red = value[2]
        green = value[1]
        blue = value[0]
    else:
        intervel = 0

    return red, green, blue
    
    


def main():
    red = 0
    green = 0
    blue = 0
    
    k = 0
    c = 0
    a = True


    new_width=400
    new_height=300

    
    C_color = (150,100,20)
    C_thickness = 3
    C_radius = 100
  

    range = 0.0
    past_duration = 0
    robot1 = robot.ARAP()
    robot1.init_devices()    
    
    
    start_time = time.time()


    cam = robot1.robot.getDevice("camera")
    cam.enable(robot1.time_step)


    while True: 

        image = cam.getImage()
        # Convert the raw Webots image to a NumPy array
        width = cam.getWidth()
        height = cam.getHeight()

        # Convert the raw byte image to a NumPy array and reshape it
        img_array = np.frombuffer(image, dtype=np.uint8).reshape((height, width, 4))  # 4 channels: BGRA
    
        
        resized_image = cv.resize(img_array,(new_width,new_height))

        cv.imshow("Original Image", resized_image)

        Cen_circle = cv.circle(resized_image,(200,150),C_radius,C_color,C_thickness)
        image_rect = cv.rectangle(Cen_circle,(120,100),(280,200),C_color,C_thickness)
        croped_img = image_rect[105:195,125:275]
        Filter_img = cv.resize(croped_img,(new_width,new_height))
        small_img = cv.resize(Filter_img,(200,100))
       

        
        
        
        cv.imshow("Complete_View", image_rect)
        cv.imshow('Filter', small_img) 

        


        end_time = time.time()
        duration = int(end_time - start_time)
        robot1.reset_actuator_values()
        
        range = robot1.get_sensor_input()
        robot1.blink_leds()
        #red, green, blue = robot1.get_camera_image(5)       #old code with-out OpenCV

        red , green , blue = extracting_data_image(Filter_img,100,100,5)  #updated code with guided fliter       
        #print(r,",",g,",",bl)


        if duration > past_duration:
            counter(duration)
        past_duration = duration
        #print(status)                                        #debug the status Condition 

    


        if (red>=200) and (green<100) and (blue<100):
            b = Red_OBS()
            if b == 1 and a == True:
                #print("Found RED Box - ", a , " " , b)
                print("Found RED BOX")
                k = pervious_box(b , a , k)
                a = False


        elif(red<100) and (green>=170) and (blue<100):
            b = Green_OBS()
            if b == 2 and a == True:
                #print("Found GREEN Box - ", a ," ", b)
                print("Found GREEN BOX")
                k = pervious_box(b , a , k)
                a = False
            
        
        elif(red<100) and (green<100) and (blue>=200):
            b = Blue_OBS()
            if b == 3 and a == True:
                #print("Found BLUE Box - ", a ," ", b)
                print("Found BLUE BOX")
                k = pervious_box(b , a , k)
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

        if cv.waitKey(1) & 0xFF == ord('q'):
            break

cv.destroyAllWindows()


if __name__ == "__main__":
    main()
    
    
