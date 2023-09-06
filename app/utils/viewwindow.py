import tkinter as tk
from tkinter import filedialog
from typing import Any
import customtkinter as ctk
import geopandas as gpd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt



class GeoPlotInformation:
    def __init__(self,
                 gdf_data = None, 
                 title = "",
                 x_ax_label = "",
                 y_ax_label = "", 
                 column = "precinct",                 
                 color = "tab20", 
                 axes: bool = False,
                 heat_bar: bool = False, 
                 vmin_max_set: bool = False, 
                 vmin: float = 0, 
                 vmax: float = 0,
                 epsg_code = None):
        self.gdf_data = gdf_data
        self.title = title
        self.x_ax_label = x_ax_label
        self.y_ax_label = y_ax_label
        self.column = column
        self.color = color
        self.axes = axes
        self.heat_bar = heat_bar
        self.vmin_max_set = vmin_max_set
        self.vmin = vmin 
        self.vmax = vmax
        self.epsg_code =epsg_code
       
    def __str__(self):
        return (f"GeoPlotInformation Object containing"
                f"\n\ttitle = {self.title}"
                f"\n\tx-axis label = {self.x_ax_label}"
                f"\n\ty-axis label = {self.y_ax_label}"
                f"\n\tcolumn = {self.column}"
                f"\n\tcolor = {self.color}"
                f"\n\taxes = {self.axes}"
                f"\n\theat_bar = {self.heat_bar}"
                f"\n\tvmin_max_set = {self.vmin_max_set}"
                f"\n\tvmin = {self.vmin}"
                f"\n\tvmax = {self.vmax}"
                f"\n\tespg_code = {self.epsg_code}") 


class GeoGraphFrame(ctk.CTkFrame):
    def __init__(self, plot_info: GeoPlotInformation, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.geometry("800x600")
       
        self.plot_info = plot_info
       
        self.gdf = plot_info.gdf_data 
        
        # self.gdf = gpd.read_file("/home/peter/Dropbox/Coding_Projects/GerryMandering_Stuff/Redist_Review/VA_precincts.zip")
        
        self.fig, self.ax = plt.subplots()

        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side="top", fill="both", expand=1)    
      
      
        self.save_button = ctk.CTkButton(self, text="Save Plot",command=self.save_plot)
        self.save_button.pack(side="bottom",padx = 20, pady=20) 
        
        self.plot()

        # self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        self.canvas.get_tk_widget().destroy()
        self.canvas.get_tk_widget().pack_forget()
        # need to close the matplot lib figure and quit the tk event loop explicitly
        plt.close(self.fig)
        del self.ax
        del self.fig
        del self.canvas
        self.destroy() 

    def plot(self):
        self.canvas.get_tk_widget().destroy()

        self.fig, self.ax = plt.subplots()

        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side="top", fill="both", expand=1)
       
        if not self.plot_info.vmin_max_set: 
            self.gdf.plot(column=self.plot_info.column, 
                          ax=self.ax, 
                          cmap=self.plot_info.color, 
                          legend=self.plot_info.heat_bar)
        else:
            self.gdf.plot(column=self.plot_info.column, 
                          ax=self.ax, 
                          cmap=self.plot_info.color, 
                          vmin=self.plot_info.vmin,
                          vmax=self.plot_info.vmax,
                          legend=self.plot_info.heat_bar) 
    
    
        if not self.plot_info.axes:
                plt.axis("off")
        
        plt.title(self.plot_info.title)

        self.canvas.draw()

    def save_plot(self):
        filename = filedialog.asksaveasfilename(defaultextension=".png")

        if filename:
            plt.savefig(filename)
    
    def update(self, plot_info: GeoPlotInformation):
        self.plot_info = plot_info
        self.plot()
