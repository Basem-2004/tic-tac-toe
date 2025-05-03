import customtkinter as ctk
from settings import *
try:
    import ctypes
except:
    pass

class App(ctk.CTk):
    def __init__(self):
        super().__init__(fg_color= "#121212")
        
        # set up
        self.title("")
        self.geometry(f"{SIZE[0]}x{SIZE[1]}+{int(self.winfo_screenwidth() / 2 - SIZE[0] / 2)}+{int(self.winfo_screenheight() / 2 - SIZE[1] / 2)}") 
        self.minsize(SIZE[0], SIZE[1])
        self.iconbitmap("empty.ico")  
        self.change_title_bar_color()
        
        # layout
        self.columnconfigure((0, 1, 2), weight= 1, uniform= "a")   
        self.rowconfigure((0, 1, 2), weight= 1, uniform= "a")   
        
        # data
        self.turn = ctk.BooleanVar(value= True)
        self.win = ctk.BooleanVar(value= False)
        self.buttons = []
        self.used_buttons = []
        self.characters = ["X", "O"]
        
        # widgets
        self.create_buttons()
        self.mainloop()
    
    def create_buttons(self):
        main_font = ctk.CTkFont(family= FONT, size= TEXT_SIZE)
        for row in range(3):
            for col in range(3):
                self.buttons.append(
                    Button(
                    parent= self,
                    turn= self.turn,
                    win = self.win,
                    buttons = self.buttons,
                    used_buttons= self.used_buttons,
                    characters = self.characters,
                    font= main_font,
                    col= col,
                    row= row
                )
                )
                                 
    def check_win(self):
        win_ways = [
            # Horizontally
            [self.buttons[0], self.buttons[1], self.buttons[2]], [self.buttons[3], self.buttons[4], self.buttons[5]], [self.buttons[6], self.buttons[7], self.buttons[8]],
            
            # Vertically
            [self.buttons[0], self.buttons[3], self.buttons[6]], [self.buttons[1], self.buttons[4], self.buttons[7]], [self.buttons[2], self.buttons[5], self.buttons[8]],
            
            # Diagonally 
            [self.buttons[0], self.buttons[4], self.buttons[8]], [self.buttons[2], self.buttons[4], self.buttons[6]]
        ]
        for i in win_ways:
            if i[0].cget("text") == i[1].cget("text") == i[2].cget("text") and i[0].cget("text") != " ":
                self.win.set(True)
                i[0].configure(fg_color = WIN_COLOR)
                i[1].configure(fg_color = WIN_COLOR)
                i[2].configure(fg_color = WIN_COLOR)
                self.buttons[0].disabled_buttons()
                MessageWindow(parent= self, turn = self.turn, message="Winner:")
                
        self.check_draw()
        
    def check_draw(self):
        if len(self.used_buttons) == 9 and self.win.get() == False:   
            self.buttons[0].disabled_buttons()
            MessageWindow(parent= self, turn = self.turn)
    
    def restart(self, message_window):
        message_window.destroy()
        
        self.turn.set(value= True)
        self.win.set(value= False)
        self.used_buttons.clear()
        
        for i in self.buttons:
            i.configure(state = "normal", fg_color = DEFAULT, hover_color = RED_HOVER, text = " ")
                
    def change_title_bar_color(self):
        try:   
            hwnd = ctypes.windll.user32.GetParent(self.winfo_id())
            DWMWA_CAPTION_COLOR = 35
            COLOR = TITLE_BAR_HEX_COLORS
            ctypes.windll.dwmapi.DwmSetWindowAttribute(
                hwnd,
                DWMWA_CAPTION_COLOR,
                ctypes.byref(ctypes.c_int(COLOR)),
                ctypes.sizeof(ctypes.c_int)
            ) 
        except:
            pass   

class Button(ctk.CTkButton):
    def __init__(self, parent, font, col, row, turn, win, buttons, characters, used_buttons):
        super().__init__(
            master= parent,
            text= " ",
            font= font,
            fg_color= DEFAULT,
            hover_color= RED_HOVER,
            command= self.handle_turn
            )
        self.grid(column = col, row = row, sticky = "nswe", padx = 1, pady = 1)
        
        # data
        self.buttons = buttons
        self.used_buttons = used_buttons
        self.characters = characters
        self.turn = turn
        self.win = win
    
    def handle_turn(self):
        if self.cget("text") == " ":
            self.used_buttons.append(self)

            if self.turn.get():
                self.configure(text = self.characters[0], fg_color = X_PLAYER, hover_color = RED_HOVER)
            else:
                self.configure(text = self.characters[1], fg_color = O_PLAYER, hover_color = BLUE_HOVER)

            self.turn.set(not self.turn.get())

            new_hover = RED_HOVER if self.turn.get() else BLUE_HOVER
            for btn in self.buttons:
                if btn not in self.used_buttons:
                    btn.configure(hover_color = new_hover)
                    
            self.master.check_win() 
            
    def disabled_buttons(self):
        for i in self.buttons:
            i.configure(state = "disabled")    

class MessageWindow(ctk.CTkToplevel):
    def __init__(self, parent, turn, message = "it's a draw!"):
        super().__init__(fg_color= "#121212") 
        self.title(" ")
        self.geometry(f"200x120+{int(self.winfo_screenwidth() / 2 - 200 / 2)}+{int(self.winfo_screenheight() / 2 - 120 / 2)}")
        self.attributes("-topmost", True)
        self.overrideredirect(True) 
        self.message = message
        self.turn = turn
        
        messege_label = ctk.CTkLabel(self, 
                                 text= f"X {self.message}" if self.turn.get() == False else f"O {self.message}", 
                                 font= ("Helvetica", 16, "bold"))
    
        messege_button = ctk.CTkButton(self, 
                                   text= "OK", 
                                   fg_color= "#0006b3", 
                                   hover_color= "#00059c", 
                                   corner_radius= 12,
                                   font= ("Helvetica", 12, "bold"), 
                                   command= lambda: parent.restart(self))
    
        if self.message == "Winner:":
            messege_label.configure(text= f"{self.message} Player 1 (X)" if self.turn.get() == False else f"{self.message} Player 2 (O)", text_color= "#33b300")
        else: #for draw
            messege_label.configure(text= self.message, text_color= "white")
        
        messege_label.place(relx= 0.5, rely= 0.4, anchor= "center")
        messege_button.place(relx= 0.5, rely= 0.7, anchor= "center")    

App()