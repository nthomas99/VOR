#!/usr/bin/python

import sys
import smbus
import time
import math
from LSM9DS0 import *
import datetime
bus = smbus.SMBus(1)

IMU_upside_down = 0 	# Change calculations depending on IMu orientation. 
						# 0 = Correct side up. This is when the skull logo is facing down
						# 1 = Upside down. This is when the skull logo is facing up 
						
						
RAD_TO_DEG = 57.29578
M_PI = 3.14159265358979323846
G_GAIN = 0.070  	# [deg/s/LSB]  If you change the dps for gyro, you need to update this value accordingly


def writeGRY(register,value):
        bus.write_byte_data(GYR_ADDRESS, register, value)
        return -1


def readGYRx():
        gyr_l = bus.read_byte_data(GYR_ADDRESS, OUT_X_L_G)
        gyr_h = bus.read_byte_data(GYR_ADDRESS, OUT_X_H_G)
        gyr_combined = (gyr_l | gyr_h <<8)

        return gyr_combined  if gyr_combined < 32768 else gyr_combined - 65536
  

def readGYRy():
        gyr_l = bus.read_byte_data(GYR_ADDRESS, OUT_Y_L_G)
        gyr_h = bus.read_byte_data(GYR_ADDRESS, OUT_Y_H_G)
        gyr_combined = (gyr_l | gyr_h <<8)

        return gyr_combined  if gyr_combined < 32768 else gyr_combined - 65536

def readGYRz():
        gyr_l = bus.read_byte_data(GYR_ADDRESS, OUT_Z_L_G)
        gyr_h = bus.read_byte_data(GYR_ADDRESS, OUT_Z_H_G)
        gyr_combined = (gyr_l | gyr_h <<8)

        return gyr_combined  if gyr_combined < 32768 else gyr_combined - 65536



#initialise the gyroscope
writeGRY(CTRL_REG1_G, 0b00001111) #Normal power mode, all axes enabled
writeGRY(CTRL_REG4_G, 0b00110000) #Continuos update, 2000 dps full scale

gyroXangle = 0.0
gyroYangle = 0.0
gyroZangle = 0.0
	
a = datetime.datetime.now()


time.sleep(5)
loop_count = 0
head_data = []

print "entering loop"

while loop_count <= 1500:
	
	
	#Read the accelerometer,gyroscope and magnetometer values
	GYRx = readGYRx()
	GYRy = readGYRy()
	GYRz = readGYRz()
		
	##Calculate loop Period(LP). How long between Gyro Reads
	b = datetime.datetime.now() - a
	a = datetime.datetime.now()
	LP = b.microseconds/(1000000*1.0)
	#print "Loop Duration | %5.2f|" % ( LP ),
	
		
	#Convert Gyro raw to degrees per second
	rate_gyr_x =  GYRx * G_GAIN
	rate_gyr_y =  GYRy * G_GAIN
	rate_gyr_z =  GYRz * G_GAIN


	#Timestamp for loop

	IMU_timestamp = time.time()


	if 1:   			#Change to '0' to stop showing time
		head_data.append(str("timestamp,%s" % (IMU_timestamp)) + ","),

	if 1:           #Change to '0' to stop showing the degrees per second from the gyro
		head_data.append(str("GRYX DPS,%5.2f,GYRY DPS,%5.2f,GYRZ DPS,%5.2f" % (rate_gyr_x,rate_gyr_y,rate_gyr_z)) + ","),


	#slow program down a bit, makes the output more readable
	time.sleep(0.03)

	loop_count += 1
print "Loop complete"

with open("IMU_output.txt", "w") as IMU_output:
	IMU_output.write(str(head_data))

print "The end"
