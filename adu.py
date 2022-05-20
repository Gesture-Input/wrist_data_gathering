import serial
import time

ser = serial.Serial('COM7',9600)
time.sleep(2)

id = 1
id = str(id)

print(id)

while True:
	res = ser.readline()
	print(res.decode()[:len(res)])
