import tkinter as tk
import customtkinter as ctk


class MinMaxSliderFrame(ctk.CTkFrame):
    def __init__(self, 
                 master, 
                 min_value = 0,
                 min_value_name = "",
                 max_value = 1,
                 max_value_name = "",
                 update_button_name = "Update",
                 update_button_command = None,
                 **kwargs):
        super().__init__(master, **kwargs)
        
        
        self.update_command = update_button_command
         
        self.min_slider = ctk.CTkSlider(self, 
                                        from_=min_value, 
                                        to=max_value, 
                                        command=self.min_slider_bounds_check)
        self.min_slider.set(min_value)
        self.min_slider_label = ctk.CTkLabel(self, 
                                             text = min_value_name + f" = {self.min_slider.get():.2f}")
        self.max_slider = ctk.CTkSlider(self, 
                                        from_=min_value, 
                                        to=max_value, 
                                        command=self.max_slider_bounds_check)
        self.max_slider.set(max_value)
        self.max_slider_label = ctk.CTkLabel(self, 
                                             text = max_value_name + f" = {self.max_slider.get():.2f}")
        
        self.update_button = ctk.CTkButton(self, text=update_button_name)
        
        if update_button_command is not None:
            self.update_button.configure(command = update_button_command)
            
        self.min_slider_label.pack(side="top", pady=5)
        self.min_slider.pack(side="top", pady=5)
        self.max_slider_label.pack(side="top", pady=5)
        self.max_slider.pack(side="top", pady=5)
        self.update_button.pack(side="top", pady=5)
        
    def min_slider_bounds_check(self, _):
        if self.min_slider.get() > self.max_slider.get():
            self.max_slider.set(self.min_slider.get())
        self.min_slider_label.configure(text=f"Min val Heatmap = {self.min_slider.get():.2f}")
        self.max_slider_label.configure(text=f"Man val Heatmap = {self.max_slider.get():.2f}")
   
    
    def max_slider_bounds_check(self,_): 
        if self.min_slider.get() > self.max_slider.get():
            self.min_slider.set(self.max_slider.get()) 
        self.min_slider_label.configure(text=f"Min val Heatmap = {self.min_slider.get():.2f}")
        self.max_slider_label.configure(text=f"Man val Heatmap = {self.max_slider.get():.2f}")
    
    def get_min(self):
        return self.min_slider.get()
    
    def get_max(self):
        return self.max_slider.get()

    def set(self, min_val: float, max_val: float):
        self.min_slider.set(min_val)
        self.max_slider.set(max_val)
        self.min_slider_label.configure(text=f"Min val Heatmap = {self.min_slider.get():.2f}")
        self.max_slider_label.configure(text=f"Man val Heatmap = {self.max_slider.get():.2f}")

    def set_from_to(self, from_val: float, to_val:float):
        self.min_slider.configure(from_=from_val, to=to_val)
        self.max_slider.configure(from_=from_val, to=to_val)

    def disable(self):
        self.min_slider.configure(state="disabled")
        self.min_slider_label.configure(text_color="grey")
        self.max_slider.configure(state="disabled")
        self.max_slider_label.configure(text_color="grey")
        self.update_button.configure(state="disabled", fg_color="#144870")
         
