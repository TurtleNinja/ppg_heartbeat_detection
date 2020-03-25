import traceback
import time

from my_wearable.ble import BLE
from my_wearable.ppg import PPG

""" -------------------- Settings -------------------- """
run_config = False                # whether to config PC HM-10 or not
baudrate = 9600                   # PySerial baud rate of the PC HM-10
serial_port = "/dev/cu.usbserial-0001"   # Serial port of the PC HM-10
peripheral_mac = "78DB2F141044"   # Mac Address of the Arduino HM-10

signal_len = 10  # length of signal in seconds (start with 10)
sample_rate = 33.3                  # samples / second
buff_len = round(signal_len*sample_rate) # length of the data buffers
plot_refresh = 20                 # draw the plot every X samples (adjust as needed)

""" -------------------- Test #1 -------------------- """
"""
ppg = PPG(buff_len, sample_rate)

hm10 = BLE(serial_port, baudrate, run_config)
hm10.connect(peripheral_mac)

# remove the first value because it is usually incomplete
try:
   msg = hm10.read_line(eol = ";")
except KeyboardInterrupt:
   print("\nExiting due to user input (<ctrl>+c).")
   hm10.close()
except Exception:
   print("\nExiting due to an error.")
   traceback.print_exc()
   hm10.close()

try:
    counter = 0
    while(True):
        msg = hm10.read_line(';')
        print(msg)
        if len(msg) > 0:
            ppg.append(msg)
            if counter % plot_refresh == 0:
                ppg.plot_live()
            counter += 1
except KeyboardInterrupt:
    print("\nExiting due to user input (<ctrl>+c).")
    hm10.close()
except Exception as e:
    print("\nExiting due to an error.")
    traceback.print_exc()
    hm10.close()

"""
""" -------------------- Test #2 -------------------- """

ppg = PPG(buff_len, sample_rate)
ppg.load_file("objective2/PPGRaw1.csv")
ppg.process()
