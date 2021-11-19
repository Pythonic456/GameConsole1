import tkinter as tk

class console:
    def __init__(self, led_width=5, led_height=5, buttons=4):
        self.__root = tk.Tk()
        self.__root.title('Console')
        self.__states = {0:'black',1:'white'}
        self.create_buttons(buttons)
        self.create_leds(led_height, led_width)
        self.width = led_width
        self.height = led_height
    def create_buttons(self, num):
        self.buttons = []
        self.button_frame = tk.Frame(self.__root)
        for i in range(num):
            button = {'button': tk.Button(self.button_frame, text=str(i+1))}
            button['button'].grid(column=i, row=0)
            self.buttons.append(button)
        self.button_frame.pack(side='bottom')
    def assign_button(self, button_num, command, sequence=None):
        self.buttons[button_num]['button'].config(command=command)
        self.__root.bind(sequence, command)
    def create_leds(self, width, height):
        self.leds = []
        self.led_frame = tk.Frame(self.__root)
        for i in range(height):
            row_leds = []
            for b in range(width):
                led = tk.Frame(self.led_frame, bg=self.__states[0], width=10, height=10) #, text='+' , fg=self.__states[0]
                led.grid(column=i, row=b)
                row_leds.append([led,0])
            self.leds.append(row_leds)
        self.led_frame.pack(side='top')
    def set_led(self, column, row, state):
        if self.leds[column][row][1] == state: return
        self.leds[column][row][0].config(bg=self.__states[state])#,fg=self.__states[state])
        self.leds[column][row][1] = state
    def set_all_leds(self, state):
        for i in range(self.height):
            for b in range(self.width):
                if self.leds[i][b][state] != state:
                    self.set_led(i,b,state)
    def after(self, ms, command):
        return self.__root.after(ms, command)
    def after_cancel(self, afterif):
        return self.__root.after_cancel(afterif)
    def start_loop(self):
        self.__root.mainloop()