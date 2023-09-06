import tkinter as tk
import customtkinter as ctk

class RadialSelectFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, list_name = "Item List", item_list = [], command=None, **kwargs):
        super().__init__(master, **kwargs)

        self.command = command
        self.radiobutton_variable = ctk.StringVar()
        self.radiobutton_list = []
        
        self.list_label = ctk.CTkLabel(self, text =  "    " +  list_name + "    ", fg_color="#333333")

        self.list_label.pack(side="top", pady=10)
        for i, item in enumerate(item_list):
            self.add_item(item)

        # Make it so that we select the first item in the list automatically.
        self.radiobutton_variable.set(item_list[0])

    def add_item(self, item):
        radiobutton = ctk.CTkRadioButton(self, text=item, value=item, variable=self.radiobutton_variable)
        if self.command is not None:
            radiobutton.configure(command=self.command)
        # radiobutton.grid(row=len(self.radiobutton_list), column=0, pady=(0, 10))
        radiobutton.pack(side="top", pady=(0,10))
        self.radiobutton_list.append(radiobutton)

    def get_checked_item(self):
        return self.radiobutton_variable.get()
    
class CheckBoxFrame(ctk.CTkFrame):
    def __init__(self, master, check_name = "Checkbox", command = None, **kwargs):
        super().__init__(master, **kwargs)
        
        self.command = command
        self.checkbox = ctk.CTkCheckBox(self, text= check_name, onvalue = 1, offvalue = 0)
        
        if self.command is not None:
            self.checkbox.configure(command = self.command)
        
        self.checkbox.pack(side="top", fill="both", expand=True, padx=20, pady=20)
        
    def get_value(self):
        if self.checkbox.get() == 1:
            return True
        return False

    
    def select(self):
        self.checkbox.select()

    def deselect(self):
        self.checkbox.deselect()
        
    def disable(self):
        if self.checkbox.get() == 1:
            self.checkbox.deselect()
        self.checkbox.configure(text_color="grey", state=tk.DISABLED, fg_color="#144870" )
