import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


############################################################
#                   CONFIGURAION                           #
############################################################

meat_points = 70 # Number of point inside meat
desired_int_temp = 40 # The internal temperature at which heating stops
ambient_temp = 20 # Temperature of the air and temperature of the meat before cookig
pan_temp=110 # Temperature of the frying pan
c = 0.3 #diffusion coefficient
h = 0.01 #diffusion coefficient for air boundary
num_frames = 3000  # Number of frames for the simulation
flipping_interval=200 # How ofter to flip the meat

settings="Configuration:"+ "\n"
settings+="points="+str(meat_points) + "\n"
settings+= "c="+str(c)+ "\n"
settings+= "h="+str(h)+ "\n"
settings+="desired_int_temp="+str(desired_int_temp)+ "\n"
settings+= "pan_temp="+str(pan_temp)+ "\n"
settings+= "flipping_interval="+str(flipping_interval)+ "\n"
settings+= "ambient_temp="+str(ambient_temp)+ "\n"
settings+= "num_frames="+str(num_frames)+ "\n"


which_side_on_pan = True
desired_int_temp_reached=False
meat = np.zeros(meat_points)
for i in range(meat_points):
    meat[i] = ambient_temp



############################################################
#              Main simulation function                    #
############################################################

def heat_transfer_simulation(_meat, heat_source_index=None):
    global ambient_temp,c,h,pan_temp
    n = len(_meat)
    anew = np.copy(_meat)
        
    

    # Apply boundary conditions:
    if heat_source_index == 0:  # Left side heated
        anew[0] = pan_temp  # Maintain heat
        anew[n - 1] = _meat[n - 1] - h * (_meat[n - 1] - ambient_temp)

    elif heat_source_index == n - 1:  # Right side heated
        anew[n - 1] = pan_temp  # Maintain heat
        anew[0] = _meat[0] - h * (_meat[0] - ambient_temp)

    else:  # No active heat source, both ends cool naturally
        ambient_temp = 20
        anew[0] = _meat[0] - h * (_meat[0] - ambient_temp)
        anew[n - 1] = _meat[n - 1] - h * (_meat[n - 1] - ambient_temp)

   
   #          This for loop does the simulation               #
    for i in range(1, n - 1):
        anew[i] = _meat[i] + c * (_meat[i - 1] - 2 * _meat[i] + _meat[i + 1])


    return anew








############################################################
#                 Stuff for the plots                      #
############################################################


fig, (Graph1, Graph2) = plt.subplots(1, 2, figsize=(12, 6))  # Two plots side by side
line, = Graph1.plot(meat)
line2, = Graph2.plot(meat)
Graph1.set_xlabel("Position")
Graph1.set_ylabel("Temperature °C")
Graph1.set_title("Meat temperature profile")
Graph1.set_ylim(0, pan_temp+10)  
Graph2.set_title("Temperature at the center")
Graph2.set_xlabel("Time")
Graph2.set_ylabel("Temperature °C")
Graph2.set_xlim(0, num_frames)  
Graph2.set_ylim(0, pan_temp+10)  
time_data = []  # List to store time (frames)
temp_data = []  # List to store temperature at len(a)//2
heat_source_line, = Graph1.plot([0, 0], [0, 140], color='red', linestyle='-', linewidth=4)
marker_Graph1_T_reached, = Graph1.plot([], [], 'bo', markersize=8, label=str(desired_int_temp) +"°C Reached")     # Marker for first plot
marker_Graph2_T_reached, = Graph2.plot([], [], 'bo', markersize=8, label=str(desired_int_temp) +"°C Reached")  # Marker for second plot
marker_Graph2_MAX, = Graph2.plot([], [], 'ro', markersize=8, label="Max Internal Temp")
marker_Graph1_MAX, = Graph1.plot([], [], 'ro', markersize=8, label="Max Internal Temp")
max_temp_text = Graph2.text(0, 0, '', color='red', fontsize=10, verticalalignment='bottom', horizontalalignment='left')
desired_temp_text = Graph2.text(0, 0, '', color='blue', fontsize=10, verticalalignment='bottom', horizontalalignment='left')









def animate(frame):
    global meat, desired_int_temp, desired_int_temp_reached,num_frames,flipping_interval,which_side_on_pan
    if frame >= num_frames-1:
        ani.event_source.stop()  # Stop the animation when max frames reached
        return
    
    # Flip the meat if it is time to do so
    if frame % flipping_interval == 0 and frame > 20:
        if which_side_on_pan:
         which_side_on_pan = False
        else:
         which_side_on_pan = True
    # get the position of frying pan (left or right)
    if which_side_on_pan:
        heat_source_index = 0
    else:
        heat_source_index = meat_points - 1
    
    # And now we cook!
    if meat[len(meat)//2] < desired_int_temp and desired_int_temp_reached==False:
        meat = heat_transfer_simulation(meat, heat_source_index) # run simulation with heat sorce
        heat_source_line.set_data([heat_source_index, heat_source_index], [0, 140])
        heat_source_line.set_visible(True)
        marker_Graph1_T_reached.set_visible(False)
        marker_Graph2_T_reached.set_visible(False)
        desired_temp_text.set_visible(False) 

    else: # when internal temperature is reached
        
        meat = heat_transfer_simulation(meat) # run simulation without heat sorce
        if not desired_int_temp_reached:# this runs only once
            marker_Graph2_T_reached.set_data([frame], [meat[len(meat)//2]])
            desired_int_temp_reached = True

            # Update text at marker_2's position
            desired_temp_text.set_position((frame, meat[len(meat)//2]))
            desired_temp_text.set_text(" Desired Temp " +  str(desired_int_temp)+ "°C. Heating stops")
            desired_temp_text.set_visible(True)
            heat_source_line.set_visible(False)
            marker_Graph1_T_reached.set_data([len(meat)//2], [desired_int_temp])
            marker_Graph1_T_reached.set_visible(True)
            marker_Graph2_T_reached.set_visible(True)

    # Update stuff for the plot
    line.set_ydata(meat)
    time_data.append(frame)
    temp_data.append(meat[len(meat)//2])
    line2.set_data(time_data, temp_data)    
    max_temp = max(temp_data)
    max_index = temp_data.index(max_temp)
    max_time = time_data[max_index]
    marker_Graph2_MAX.set_data([max_time], [max_temp])
    marker_Graph2_MAX.set_visible(True)
    marker_Graph1_MAX.set_data([len(meat)//2], [max_temp])
    marker_Graph1_MAX.set_visible(True)
    max_temp_text.set_position((max_time, max_temp))
    max_temp_text.set_text(f"Max Temp: {int(round(max_temp))}°C")

    return line, line2, marker_Graph1_T_reached, marker_Graph2_T_reached, marker_Graph2_MAX, marker_Graph1_MAX, heat_source_line, max_temp_text, desired_temp_text




# Create the animation
ani = animation.FuncAnimation(fig, animate, frames=num_frames, interval=1, blit=True)  # interval in milliseconds

fig.text(0.28, 0.17, 
         "Jumping red line represent \n"
         "flipping of the frying pan\n",     
         ha='center', va='top', fontsize=12, fontweight='bold')
fig.text(0.85, 0.91, 
         settings,     
         ha='left', va='top', fontsize=9, )
plt.tight_layout()  
plt.show()
