import time
import sys
import webbrowser
import os

url = "https://www.youtube.com/watch?v=dlcOORQFN2g"
print("Number of arguments:" + str(len(sys.argv)))
print("Python scripts arguments" + str(sys.argv))

hours = int(sys.argv[1])
minutes = int(sys.argv[2])
seconds = int(sys.argv[3])

Set_Alarm = "{:02d}:{:02}:{:02d}".format(hours, minutes, seconds)
Actual_Time = time.strftime("%H:%M:%S")
print("Now: " + Actual_Time)
print("Set Alarm at: " + Set_Alarm)

while (Actual_Time != Set_Alarm):  
    Actual_Time = time.strftime("%H:%M:%S")  
    time.sleep(1)
    
if (Actual_Time >= Set_Alarm):  
    print ("Time's up") 
    webbrowser.open(url)
    os._exit(0)
    
    # We are calling the open()  
    # function from the webrowser module.  