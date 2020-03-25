Vy Truong
A16103482

# Lab 6

## Introduction
*This lab incorporates a hear beats monitor for the embedded device*

## Objective 1
* Build an IR circuit that connects to Arduino*

Steps completed:
* Built an IR circuit and connected it to Arduino
* Test the circuit using an Aruidno sketch for IR


## Objective 2
*Develop a program collecting data from IR which was collected and sent over BLE by Arduino. Experiment with visualizing data live*

Steps completed:
* Write an Arduino program reading IMU and IR signals and procasting over BLE
* Develop the `ppg.py` class in `my_wearable` library to read IR data from BLE, save it to file and plot from file.
* Develop a feature in `ppg.py` that allows live plotting as data was received via BLE

[`PPG.csv`](https://github.com/UCSD-Product-Engineering/ece16-fa19-TurtleNinja/blob/master/lab6/objective2/PPG.csv "PPG.csv")


## Objective 3
*Develop filter mechanism for IR data collected*

Steps completed:
* Collected five sets of IR data
* Wrote code for low-pass, high-pass, de-meaning filter for PPG
* Experiment multiple cutofff frequencies for filters with different sets of data to get the optimal cutoff values.
    
[csv data files](https://github.com/UCSD-Product-Engineering/ece16-fa19-TurtleNinja/tree/master/lab6/objective3)
    
## Objective 4
*Develop a method to detect heartbeats from IR data*

Steps completed:
* Wrote method `__find_heartbeats()` that detects and collects heartbeats signal from raw data
    * Filtered raw data: remove drift, bandpass filtering and taking gradient
    * Experimented with cutoff threshold and collected peaks in processed data that pass an optimal threshold
    * Visualized filtered data with peaks marked on the plot
    
    
## Objective 5
*Implement sliding window for live data processing*

Steps completed:
* Modified `__find_heartbeats()` method to processed collected data in windows



## Conclusion
*This lab developed method to use infared light to detect heartbeats*

New things I have learned in this lab:
* Infared light machanism in detecting heartbeats
* Signal processing using sliding window
* Live plotting data using Python Mathlotlib

Problems and solutions:
* *Objective 2:*
* IR circuit was not efficent because I did not arrange the emitter and receiver well
After objective 1, I rewired the circuit, and the IR emitter and receiver was put too close to each other. It results in a very week signal, and one I have my finger cover the light, the signal is nearly 0. I kept thinking the hardware itself had issue. Then I experimented things by using different fingers, changing their distance and I found a good distance.
* Sampling frequency was incompatible with my hardward
The suggested sampling frequency was too high for my laptop's processor, so the data received in the Python side was defective. Jane suggested me to decrease the frequency and it worked.
* Live plotting froze
There was an issue with my IR circuit that lead to invalid data plotted on the Python side. I could not figure out where the bug was, so I changed code randomly and I copied the infinite loop code from the lecture for my live plotting. My program became froze after the first data received. Professor Ramsin helped me debugged this and the program worked well.

* *Objective3* 
* Minor fag in the Python program
I program `main.py` so that it will plot and save the plot by itself. While letting the program plotting data after every stage of filtering of all five data sets, the program flags that there are too many figures was created. And also, since the given code open an empty figure to detect the `enter` key signal, all the plots saved from the program was empty plot. I figured that one out and modified the program, so it close the previous figure before opening a new one.

The rest of the lab worked out smoothly without any major issue.
