import os
import serial
import numpy as np
import time
import heapq
import pyautogui.press

class wrist():
    def __init__(self,name,length):
        self.name = name
        self.data_path = "C:\\piledata\\class_data\\3학년\창의캡스톤디자인\\wrist_data_gathering\\data\\"+ name + ".txt"
        self.length = length
        self.data = []
        self.ser = serial.Serial('COM3',9600)
        self.gesture = ""
    
    def get_data(self):
        if(not os.path.exists(self.data_path)):
            print("file not exists")
            return False
        data = open(self.data_path,"r", encoding='utf-8') 
        self.data_to_numpy(data)
        data.close()
        return True
    
    def data_to_numpy(self,data):
        while True:
            line = data.readline()
            if not line: break
            temp = []
            line_data = line[:-1].split(" ")
            print(line_data)
            temp.append(line_data[0])
            temp.append(np.array(list(map(float, line_data[1:]))))
            self.data.append(temp)
        return
    
    def save_data(self):
        file = open(self.data_path, "w")
        tempstr = ""
        for temp in self.data:
            tempstr += temp[0]
            for i in temp[1].tolist():
                tempstr += " "
                tempstr += str(i)
            tempstr += "\n"
        file.write(tempstr)
        file.close()
    
    def add_input(self,input_key):
        maxcount = 50
        temp = []
        temp.append(input_key)
        count = 0
        tempdata = np.array([0,0,0,0])
        while(count < maxcount):
            res = self.ser.readline()
            print(res.decode()[:len(res)])
            print(np.array(res.decode()[:len(res)]))
            
            tempdata += np.array(list(map(int, res.decode()[:len(res)].split(" "))))
            count += 1
        
        temp.append(tempdata/maxcount)
        self.data.append(temp)
        return
    
    def calculate_gesture(self,current):
        temp_heap = []
        heapq.heapify(temp_heap)
        for i in self.data:
            diff = i[1] - current
            dis_sq = 0
            for j in diff.tolist():
                dis_sq += j * j
            heapq.heappush(temp_heap, (dis_sq, i[0]))
        return heapq.heappop(temp_heap)[1]
    
    def listen(self):
        while True:
            res = self.ser.readline()
            current = np.array(list(map(float, res.decode()[:len(res)].split(" "))))
            self.gesture = self.calculate_gesture(current)
            pyautogui.press(self.gesture)
            
    def listen_data(self):
        while True:
            res = self.ser.readline()
            print(np.array(list(map(float, res.decode()[:len(res)].split(" ")))))
        

wr1 = wrist("LightYe4r",4)
wr1.get_data()
print("데이터 확인\n")
print(wr1.data)

temp = input("데이터 불러오기 완료 입력을 시작하려면 ENTER를 누르세요")

wr1.listen()