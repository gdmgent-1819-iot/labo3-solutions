#-*- coding: utf-8 -*-

from sense_hat import SenseHat
from time import time, sleep
import os
import sys

# Constants
TEMP_CORRECTION_FACTOR = 1.5

# function: get_cpu_temp()
# get the temperature from the CPU
def get_cpu_temp():
    res = os.popen('vcgencmd measure_temp').readline()
    t = float(res.replace('temp=', '').replace("'C\n", ''))
    return(t)

# function: get_smooth(x)
# use moving average to smooth readings
def get_smooth(x):
  if not hasattr(get_smooth, "t"):
    get_smooth.t = [x,x,x]
  get_smooth.t[2] = get_smooth.t[1]
  get_smooth.t[1] = get_smooth.t[0]
  get_smooth.t[0] = x
  xs = (get_smooth.t[0]+get_smooth.t[1]+get_smooth.t[2])/3
  return(xs)

# function: get_temp(with_case)
# get the real temperature
def get_temp(with_case):
    temp_humidity = sense.get_temperature_from_humidity()
    temp_pressure = sense.get_temperature_from_pressure()
    temp = (temp_humidity + temp_pressure)/2
    if with_case:
        temp_cpu = get_cpu_temp()
        temp_corrected = temp - ((temp_cpu - temp)/TEMP_CORRECTION_FACTOR)
        temp_smooth = get_smooth(temp_corrected)
    else:
        temp_smooth = get_smooth(temp)/TEMP_CORRECTION_FACTOR
    return(temp_smooth)

try:
    # SenseHat
    sense = SenseHat()
    sense.set_imu_config(False, False, False)
except:
    print('Unable to initialize the Sense Hat library: {}'.format(sys.exc_info()[0]))
    sys.exit(1)
    
def main():
    withcase = False
    if len(sys.argv[1:]) > 0:
      v = sys.argv[1:][0]
      withcase = True if v == 'True' else False

    temp = (get_temp(withcase))
    sleep(2)
    temp = (get_temp(withcase))
    print('{}{}C'.format(temp, ''))
        
if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, SystemExit):
        print('Interrupt received! Stopping the application...')
        sys.exit(0)