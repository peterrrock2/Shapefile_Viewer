import tkinter as tk
import customtkinter as ctk

class ColorDropdownFrame(ctk.CTkFrame):
    def __init__(self, master, color = None, command=None, **kwargs):
        super().__init__(master, **kwargs)
        
        self.command = command
        
        self.color_list = ["Cool Heatmap", "Warm Heatmap", "Total Heatmap", "Qualitative 1", "Qualitative 2", "Qualitative 3"]
        self.color_dict = {"Cool Heatmap": "cool", "Warm Heatmap": "hot", "Total Heatmap": "inferno", "Qualitative 1": "tab20", "Qualitative 2": "tab20b", "Qualitative 3": "tab20c"}
        self.reverse_dict = {v:k for k,v in self.color_dict.items()}

        self.color_label = ctk.CTkLabel(self, text =  "    Color Selector    ", fg_color="#333333")
        self.color_option_menu = ctk.CTkOptionMenu(self, values=self.color_list) 
        if color is None:
            self.color_option_menu.set("Cool Heatmap")
        else:
            self.color_option_menu.set(self.reverse_dict[color])     
        
        
        if self.command is not None:
            self.color_option_menu.configure(command= self.command)
  
   
        self.color_label.pack(side="top", padx = 20, pady= (5,0))
        self.color_option_menu.pack(side="top", padx = 20, pady = 10 )
   

    def get_value(self):
        return self.color_dict[self.color_option_menu.get()]