# domain_lab

## this is a list of tools contained in the reposetory, how to use them and where to find them

### a tool to controll a device using visa -> device.py
(this class was writen with variable power supplyies in mind)
usage example:
```
import device

with device.Device(index=None[optional int]) as dev:
  #your code here...
```
using the dev object you can get get a voltage reading using
`dev.get_voltage()`

set the voltage offset of the device using
`dev.set_voltage(v:float)`

or preform a sequance of voltage changes and reads by using
`dev.set_fn(f:np.array,t:np.array,hook:function,args:list)`

#### the function will then preform the following:

* set the device voltage to the first value in f
* read the voltage from the device and record the time of meshurment
* call the hook function with the given args (i.e. hook(*args))

it will then return the hook's function return values and the voltage and time read from the device as a 2 tuple
i.e `(hool_return, voltage_time_array)`

### an asortment of image capture tools and some file managment tools writen with opencv -> process_image.py

```get_H_B_point2(H:float) -> bool```
this funciton takes an image from the connected camera (using `cv2.VideoCapture(0)`)
then uses the variables `ROOT` and `RUNFILE` stored in `constant.py` in order to save the image
in accordance with **our** predetermend file tructure (as specified below)

**our** predetermend file structure
each meshurment is saved in a run folder named run[i] where i is a monotonicly increasing integure counter
each run folder then contains the images recrded during this run named by their time of recording followed by the meshurment voltage
that is:
runs_
     |
     run1_
          |
          time0_voltage0.png
          time1_voltage1.png
          .
          .
          .
     run2_
          |...
and so on

### an asortment of image **processing** tools and some file managment tools writen with opencv -> process_assist.py

```image_process(path:str)```

the function blurring applies otsu's method and a fiew other tricks to create a "good" boolian
image and saves the result to the same path as the file with the word runs replaced with processed_runs
(see **our** predetermend file structure)

argumets:
path: path to image to be processed
