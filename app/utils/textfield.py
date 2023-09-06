import tkinter as tk
import customtkinter as ctk


class TextFieldEntryFrame(ctk.CTkFrame):
    def __init__(self, 
                 master, 
                 frame_label = "Frame Name",
                 placeholder_text = "Value", 
                 button_text = "Accept",
                 command = None,
                 **kwargs):
        super().__init__(master, **kwargs)
        
        self.command = command 
        self.field_label = ctk.CTkLabel(self, text =  "    " +  frame_label + "    ", fg_color="#333333")
        self.entry_field = ctk.CTkEntry(self, placeholder_text=placeholder_text) 
        self.update_button = ctk.CTkButton(self, text=button_text)
        
        if self.command is not None:
            self.update_button.configure(command=self.command)
        
        self.field_label.pack(side="top", padx=20, pady=5)
        self.entry_field.pack(side="top", padx=20)
        self.update_button.pack(side="top", padx=20, pady=(5,10))
       
    def get_value(self):
        return self.entry_field.get() 