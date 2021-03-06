import os
import serial
# from serial import Serial
import numpy as np
import time
import heapq
from threading import Thread


class Wrist():
    def __init__(self,name,length,port_name,port_num):
        self.name = name
        #check os
        if(os.name == "nt"):
            self.user_data_path = os.getcwd() + "\\data\\" + name +".txt" 
        else:
            self.user_data_path = os.getcwd() + "/data/" + name +".txt" 
        self.length = length
        self.pressure_data = np.array([])
        self.user_data = []
        self.ser = serial.Serial(port_name,port_num)
        self.gesture = ""
        self.maxcount = 50
        self.load_user_data()
        self.thread = Thread(target=self.update_wrist_data)
        self.thread.start()
    

    def get_user_data(self):
        # print(self.user_data)
        return self.user_data
    
    def load_user_data(self):
        if(not os.path.exists(self.user_data_path)):
            print("file not exists")
            return False
        data = open(self.user_data_path,"r", encoding='utf-8') 
        self.user_data_to_numpy(data)
        data.close()
        return True
    
    def user_data_to_numpy(self,data):
        while True:
            line = data.readline()
            if not line: break
            temp = []
            line_data = line[:-1].split(" ")
            print(line_data)
            temp.append(line_data[0])
            temp.append(np.array(list(map(float, line_data[1:]))))
            self.user_data.append(temp)
        return
    
    def save_user_data(self):
        print(self.user_data_path)
        file = open(self.user_data_path, "w")
        tempstr = ""
        for temp in self.user_data:
            tempstr += temp[0]
            for i in temp[1].tolist():
                tempstr += " "
                tempstr += str(i)
            tempstr += "\n"
        file.write(tempstr)
        file.close()
        print("data saved")
    
    def show_for_maxcount(self):
        for i in range(self.maxcount):
            if(self.update_wrist_data()):
                print(self.pressure_data)
    
    def add_gesture(self,gesture_name):
        self.show_for_maxcount()
        temp = []
        temp.append(gesture_name)
        count = 0
        tempdata = np.array([0.0,0.0,0.0,0.0])
        while(count < self.maxcount):
            # print(res.decode()[:len(res)])
            # print(np.array(res.decode()[:len(res)]))
            if(self.update_wrist_data()):
                tempdata += self.pressure_data
                print(self.pressure_data)
                count += 1
        temp.append(tempdata/self.maxcount)

        is_data = False
        for i in range(len(self.user_data)):
            if(self.user_data[i][0] == gesture_name):
                self.user_data[i] = temp
                is_data = True
                break
        if(not is_data):
            self.user_data.append(temp)
        return True
    
    def calculate_gesture(self,current):
        temp_heap = []
        heapq.heapify(temp_heap)
        # print(current)
        cur = np.array([0.0,0.0,0.0,0.0]) + current
        for i in self.user_data:
#             print(i)
            diff = i[1] - cur
            dis_sq = 0
            for j in diff.tolist():
                dis_sq += j * j
            heapq.heappush(temp_heap, (dis_sq, i[0]))
        return heapq.heappop(temp_heap)[1]

    def update_wrist_data(self):
        self.ser.reset_input_buffer()
        res = self.ser.readline()
        # print(res)
        try:
            temp_data = np.array(list(map(float, res.decode()[:len(res)].split(" "))))
            if(len(temp_data) == self.length):
                self.pressure_data = temp_data
            else:
                self.pressure_data = np.array([0.0,0.0,0.0,0.0])
        except:
            print("no data")
            self.pressure_data = np.array([0.0,0.0,0.0,0.0])
            return False
        
        return True
    
    def listen(self):
        if(self.update_wrist_data()):
            self.gesture = self.calculate_gesture(self.pressure_data)
        # self.gesture = self.calculate_gesture(self.pressure_data)
        
        return self.gesture
            
    def listen_data(self):
        if(self.update_wrist_data()):
            print(self.pressure_data)
        # return self.pressure_data
        
    # def empty_data(self):
    #     self.ser.readlines()