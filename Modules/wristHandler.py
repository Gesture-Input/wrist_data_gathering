from Modules import wrist
import pyautogui
# import keyboard

class WristHandler():
    class GestureHandler():
        def __init__(self):
            # self.count = 0
            self.data = ["release_vertical"]
            self.maxsize = 50
            self.current_state = ""
            self.ex_state = "" 
            
        
        def update_gesture(self,gesture):
            command = ""
            if(self.data[-1] != gesture):
                self.data_calculate(gesture)
                command = self.calculate_command()
            self.data_append(gesture)

            # if(command != ""):
            #     print("gesture command : "+command)

            return command

        def data_append(self,gesture):
            self.data.append(gesture)
            if(len(self.data) > self.maxsize):
                self.data = self.data[1:]
        
        def data_calculate(self,gesture):
            self.ex_state = self.current_state
            self.current_state = gesture

        def calculate_command(self):
            if(self.current_state == "index_finger_down_vertical"):
                if(self.ex_state == "release_vertical"):
                    return "click"
            if(self.current_state == "stretch_left_vertical"):
                if(self.ex_state == "release_vertical" or self.ex_state == "stretch_right_vertical"):
                    return "left"
            if(self.current_state == "stretch_right_vertical"):
                if(self.ex_state == "release_vertical" or self.ex_state == "stretch_left_vertical"):
                    return "right"
            if(self.current_state == "paper_vertical"):
                if(self.ex_state == "release_vertical" or self.ex_state == "rock_vertical"):
                    return "esc"
            
            return ""


    def __init__(self,name,length_list,port_name_list,port_num_list):
        self.name = name
        self.wrist_list = []
        self.gesture_list = []
        self.gesture_handler_list = []
        self.wrist_size = 0
        for i in range(len(length_list)):
            self.wrist_list.append(wrist.Wrist(self.name+"_"+str(i),length_list[i],port_name_list[i],port_num_list[i]))
            self.gesture_handler_list.append(self.GestureHandler())
            self.gesture_list.append([])
            self.wrist_size += 1
        #  0 : base / 1 : listen / 2 : show_data
        self.state = 0;
        self.wrist_index = -1;
        self.command = ""
        
    
    def execute_command(self):
        print(self.command)
        if(self.command == "click"):
            pyautogui.click()
            return
        if(self.command != ""):
            pyautogui.press(self.command)
            return
        

    def run_console(self):
        while True:
            if(self.state == 0):
                command = self.get_command_0()
                if(command < 6 and command > -1):
                    self.handle_command_0(command)
            
            if(self.state == 1):
                for i in range(self.wrist_size):
                    self.command = self.gesture_handler_list[i].update_gesture(self.wrist_list[self.wrist_index].listen())
                    if(self.command != ""):
                        self.execute_command()
                # if keyboard.is_pressed("q"):
                #     print("quit listen")
                #     self.state = 0

            if(self.state == 2):
                # self.wrist_list[self.wrist_index].empty_data()
                print(self.wrist_list[self.wrist_index].listen(), end = " : ")
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
            return
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
                self.wrist_list[self.wrist_index].show_for_maxcount()
                self.wrist_list[self.wrist_index].add_gesture(gestureName)
            return

        if (command == 5):
            if(self.choose_wrist()):
                self.wrist_list[self.wrist_index].save_user_data()
            return


    def get_command_0(self):
        print("state 0 \ncommand list")
        print("0 : run")
        print("1 : show wrist data")
        print("2 : check current user data")
        print("3 : append wrist")
        print("4 : append gesture")
        print("5 : save gesture")
        input_data = input()
        if(input_data == ""):
            input_data = -1
        command = int(input_data)
        return command
