# Imports
import serial
from time import sleep
from time import time
from scipy import signal as sig
import numpy as np
from matplotlib import pyplot as plt

class PPG:

    # Attributes of the class PPG
    _maxlen = 0
    __time_buffer = []
    __data_buffer = []
    __lower_threshold = 0.5
    __upper_threshold = 2.5
    __heartbeats = []
    __fs = 0

    """ ================================================================================
    Constructor that sets up the PPG class. It will only run once.
    :param max len: (int) max length of the buffer
    :return: None
    ================================================================================ """
    def __init__(self, maxlen, fs):
        self.__fs = fs
        self._maxlen = maxlen
        fig = plt.figure(1)
        fig.canvas.mpl_connect('key_press_event', self.__handle_keypress)
        return

    """ ================================================================================
    A callback function that triggers when a key is pressed with the plot open
    :param event: the input event that triggered the callback
    :return: None
    ================================================================================ """
    def __handle_keypress(self, event):
        if event.key == 'enter':
            self.save_file("PPGRaw1.csv")
            plt.close(fig)

    """ ================================================================================
    Resets the PPG to default state
    :return: None
    ================================================================================ """
    def reset(self):
        self.__time_buffer = []
        self.__data_buffer = []
        return

    """ ================================================================================
    Appends new elements to the data and time buffers by parsing 'msg_str' and splitting
    it, assuming comma separation. It also keeps track of buffer occupancy. Once the
    buffer is full, it will become a circular buffer and drop samples from the beginning
    as a FIFO buffer.
    :param msg_str: (str) the string containing data that will be appended to the buffer
    :return: None
    ================================================================================ """
    def append(self, msg_str):
        timestamp = 0
        new_ppg_data = 0
        try:
            vals = msg_str.split(',')
            timestamp = int(vals[0])
            new_ppg_data = int(vals[2])
        except (ValueError, IndexError):
            print("Received invalid data")
       
        if len(self.__data_buffer) == self._maxlen:
            self.__data_buffer[:-1] = self.__data_buffer[1:]
            self.__time_buffer[:-1] = self.__time_buffer[1:]
            self.__time_buffer[-1] = timestamp
            self.__data_buffer[-1] = new_ppg_data
        else:
            self.__data_buffer.append(new_ppg_data)
            self.__time_buffer.append(timestamp)
            
        return


    """ ================================================================================
    Saves the contents of the buffer into the specified file one line at a time.
    :param filename: (str) the name of the file that will store the buffer data
    :return: None
    ================================================================================ """
    def save_file(self, filename):

        with open(filename, 'w') as file:
            for i in range(len(self.__time_buffer)):
                file.write("{},{}\n".format(self.__time_buffer[i], self.__data_buffer[i]))
        
        return


    """ ================================================================================
    Loads the contents of the file 'filename' into the time and data buffers
    :param filename: (str) the name (full path) of the file that we read from
    :return: None
    ================================================================================ """
    def load_file(self, filename):
        
        self.reset()
        count = 0

        with open(filename, 'r') as file:
            while True:
                line = file.readline()
                if not line:
                    break
                
                vals = line.rstrip().split(',')
                self.__time_buffer.append(int(vals[0]))
                self.__data_buffer.append(int(vals[1]))
                count += 1
        
        self._maxlen = count
        return


    """ ================================================================================
    Plots the data in the time and data buffers onto a figure
    :param: None
    :return: None
    ================================================================================ """
    def plot(self, filename):
        
        fig = plt.figure()
        plt.subplot(111)
        plt.title(filename)
        plt.plot(self.__time_buffer, self.__data_buffer)
        for i in self.__heartbeats:
            plt.plot(self.__time_buffer[i], self.__data_buffer[i], 'rx')
        # Save the plot
        plt.savefig(filename)
        plt.close(fig)
        
        return


    """ ================================================================================
    Live plot the data in the data buffer onto a figure and update continuously
    :param: None
    :return: None
    ================================================================================ """
    def plot_live(self):
        
        plt.cla()
        plt.plot(self.__data_buffer)
        plt.show(block=False)
        plt.pause(0.001)
        
        return
        
        
    
    """ ================================================================================
    This function runs the contents of the __data_buffer through a low-pass filter. It
    first generates filter coefficients and  runs the data through the low-pass filter.
    Note: In the future, we will only generate the coefficients once and reuse them.
    :param cutoff: (int) the cutoff frequency of the filter
    :return: None
    ================================================================================ """
    def __lowpass_filter(self, cutoff):

        b,a = sig.butter(3, cutoff, btype='low', analog=False, output='ba', fs=None)
        filtered_data = sig.lfilter(b, a, self.__data_buffer)
        self.__data_buffer = filtered_data
        
        return


    """ ================================================================================
    This function runs the contents of the __data_buffer through a high-pass filter. It
    first generates filter coefficients and runs the data through the high-pass filter.
    Note: In the future, we will only generate the coefficients once and reuse them.
    :param cutoff: (int) the cutoff frequency of the filter
    :return: None
    ================================================================================ """
    def __highpass_filter(self, cutoff):
        
        b,a = sig.butter(3, cutoff, btype='high', analog=False, output='ba', fs=None)
        filtered_data = sig.lfilter(b, a, self.__data_buffer)
        self.__data_buffer = filtered_data
        return
        


    """ ================================================================================
    Runs the contents of the __data_buffer through a de-meaning filter.
    :param: None
    :return: None
    ================================================================================ """
    def __demean_filter(self):
        # Compute the mean using a sliding window
        filtered = sig.detrend(self.__data_buffer)
        self.__data_buffer = filtered
        return
    

    """ ================================================================================
    Run through the filtering operations and heuristic methods to compute.
    For now, we will use it as our "playground" to filter and visualize the data.
    :param None:
    :return: Nothing
    ================================================================================ """
    def __filter_ppg(self):
        # remove drift
        self.__demean_filter()
        #self.plot(plotfile+"{}.png".format("dm"))
        
        # filter out high frequencies
        cutoff = 10 / (0.5 * 33.3)
        self.__lowpass_filter(cutoff)
        #self.plot(plotfile+"{}.png".format("lp"))
        
        # filter out low frequencies
        cutoff = 0.5 / (0.5 * 33.3)
        self.__highpass_filter(cutoff)
        #self.plot(plotfile+"{}.png".format("hp"))
        
        # isolate peaks
        self.__data_buffer = np.gradient(self.__data_buffer).tolist()
        #self.plot(plotfile+"{}.png".format("grad"))
        
    """ ================================================================================
    Count the number of data points passing s threshold and therefore counted as a beat
    :param None:
    :return: Nothing
    ================================================================================ """
    
    def __find_heartbeats(self):
        """
                OBJECTIVE 4
        self.__filter_ppg()
        peaks = sig.find_peaks(self.__data_buffer)[0]
        for p in peaks:
            if self.__data_buffer[p] > self.__lower_threshold and self.__data_buffer[p] < self.__upper_threshold:
                self.__heartbeats.append(p)
        """
        
        # OBJECTIVE 5
        start = 0
        window_width = int(3 * self.__fs)
        end = start + window_width
        temp_data = self.__data_buffer.copy()
        temp_filtered = []
        while end < self._maxlen:
            self.__data_buffer = temp_data[start:end]
            # filter the window
            self.__filter_ppg()
            # find the peaks
            peaks = sig.find_peaks(self.__data_buffer)[0]
            for p in peaks:
                if self.__lower_threshold < self.__data_buffer[p] < self.__upper_threshold:
                    self.__heartbeats.append(start+p)
            # recollect filtered data
            temp_filtered += self.__data_buffer
            # update window
            start = end
            end = start + window_width
            
        # reassign all filtered data to data buffer
        self.__data_buffer = temp_filtered
        if len(self.__data_buffer) < self._maxlen:
            self.__time_buffer = self.__time_buffer[:len(self.__data_buffer)]
        
        return
        
    
    """ ================================================================================
    Handle the main process of PPG class
    :param None:
    :return: Nothing
    ================================================================================ """
    def process(self):
        self.__find_heartbeats()
        self.plot("OnlineHeartbeats.png")
