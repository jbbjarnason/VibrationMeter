# Vibration Meter
## Project Objective
Suppose you have a desk in an office, you sit at your desk most of the day programming. Every now and then a collegue walks past your desk causing your desk to shake even your monitor might shake. How can you measure this vibration?
## Method
Initial idea is to use accelerometer connected to a computer which logs and analysis in real time the vibration of the floor.
## Implementation
- MPU6050 accelerometer with I2C interface
- Raspberry pi receives data
- Use Python interface https://pypi.org/project/mpu6050-raspberrypi/
- Log data with X interval and over Y time
- Fourier transform the data
- Use 10 Hz low pass filter
- Integrate signal to µm
- Inverse fourier transform
- Display the data

## Nice to have
- Camera to detect person walking by
- Supervised machine learning, classifying persons

## Dependancies
- $ pip3 install numpy
- $ pip3 install threading
- $ pip3 install scipy
- $ pip3 install matplotlib
- $ sudo apt install python3-tk

## Class interfaces
### Data collection
#### Methods

- getData()
- getSpan()
- changeSpan(s)

### Data collection periodic
#### Methods

- getData()
- getSpan()
- changeSpan(s)
- getInterval()
- changeInterval(ms)