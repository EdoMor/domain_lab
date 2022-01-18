# domain_lab

## this is a list of tools contained in the reposetory, how to use them and where to find them

### a tool to control a device using visa ⇾ device.py
(this class was written with variable power supplies in mind)
usage example:
```python
import device

with device.Device(index=None[optional int]) as dev:
  #your code here...
```
using the dev object you can get a voltage reading using
`dev.get_voltage()`

set the voltage offset of the device using
`dev.set_voltage(v:float)`

or preform a sequence of voltage changes and reads by using
`dev.set_fn(f:np.array,t:np.array,hook:function,args:list)`

#### the function will then preform the following:

* set the device voltage to the first value in f
* read the voltage from the device and record the time of measurement
* call the hook function with the given args (i.e. hook(*args))

it will then return the hook's function return values and the voltage and time read from the device as a 2 tuple
i.e. `(hool_return, voltage_time_array)`

### an assortment of image capture tools and some file management tools written with OpenCV ⇾ process_image.py

```get_H_B_point2(H:float) -> bool```
this function takes an image from the connected camera (using `cv2.VideoCapture(0)`)
then uses the variables `ROOT` and `RUNFILE` stored in `constant.py` in order to save the image
in accordance with **our** predetermined file structure (as specified below)

**our** predetermined file structure
each measurement is saved in a run folder named run[i] where i is a monotonically increasing integer counter
each run folder then contains the images recorded during this run named by their time of recording followed by the measurement voltage
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

### an assortment of image **processing** tools and some file management tools written with OpenCV ⇾ process_assist.py

```image_process(path:str)```

the function blurring applies otsu's method and a few other tricks to create a "good" Boolean
image and saves the result to the same path as the file with the word runs replaced with processed_runs
(see **our** predetermined file structure)

arguments:

path: path to image to be processed

### functions for image processing that return an image and dont save it accordign to our predetermined file structure ⇾ pca.py

`gaussian_blur_otzu(img:np.array) -> np.array`
this the function that was used to create the Boolean image

### a Hysteron variable type ⇾ Hysteron.py

```python
from hysteron import Hysteron

hyst=Hysteron(func1:function,func2:function,α:float,β:float,starting_value:float)

print(hyst(3))
```