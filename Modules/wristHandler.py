from Modules import wrist
import pyautogui
# import keyboard

class WristHandler():
    def __init__(self,name,length_list,port_name_list,port_num_list):
        self.name = name
        self.wrist_list = []
        for i in range(len(length_list)):
            self.wrist_list.append(wrist.Wrist(self.name+"_"+str(i),length_list[i],port_name_list[i],port_num_list[i]))
        #  0 : base / 1 : listen / 2 : show_data
        self.state = 0;
        self.wrist_index = -1;

    def run_console(self):
        while True:
            if(self.state == 0):
                command = self.get_command_0()
                if(command < 5 and command > -1):
                    self.handle_command_0(command)
            
            if(self.state == 1):
                self.wrist_list[self.wrist_index].listen()
                # if keyboard.is_pressed("q"):
                #     print("quit listen")
                #     self.state = 0

            if(self.state == 2):
                # print(self.wrist_list[self.wrist_index].listen(), end = " : ")
                self.wrist_list[self.wrist_index].listen_data()
                # if keyboard.is_pressed("q"):
                #     print("quit show data")
                #     self.state = 0
                

    
    def choose_wrist(self):
        print(self.wrist_list)
        print("choose wrist by index")
        self.wrist_index = int(input())
        if(self.wrist_index < len(self.wrist_list) and self.wrist_index >= 0):
            return True
        return False
    
    def handle_command_0(self, command):
        if (command == 0):
            self.state = 1
        if (command == 1):
            if(self.choose_wrist()):
                print(self.wrist_list[self.wrist_index].get_user_data())
                self.state = 2
            return
        if (command == 2):
            if(self.choose_wrist()):
                print(self.wrist_list[self.wrist_index].get_user_data())
            return
        if (command == 3):
            return
        if (command == 4):
            if(self.choose_wrist()):
                gestureName = str(input())
                print("please take gesture")
                self.wrist_list[self.wrist_index].add_gesture(gestureName)
                self.wrist_list[self.wrist_index].save_user_data()
            return


    def get_command_0(self):
        print("state 0 \ncommand list")
        print("0 : run")
        print("1 : show wrist data")
        print("2 : check current user data")
        print("3 : append wrist")
        print("4 : append gesture")


        command = int(input())
        return command
