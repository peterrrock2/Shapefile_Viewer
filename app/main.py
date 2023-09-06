import tkinter as tk
import customtkinter as ctk
from utils.selections import RadialSelectFrame, CheckBoxFrame
from utils.dropdown import ColorDropdownFrame
from utils.viewwindow import GeoPlotInformation, GeoGraphFrame
from utils.textfield import TextFieldEntryFrame
from utils.sliders import MinMaxSliderFrame
from tkinter import filedialog
import geopandas as gpd
import sys
import warnings

warnings.filterwarnings("ignore")

class ShapeFileViewer(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Shapefile Viewer")

        self.geometry("180x75") 

        self.get_file_button = ctk.CTkButton(self, 
                                             text="Click to load Shapefile", 
                                             command=self.get_file_name)
        
        self.get_file_button.grid(row = 0, column = 0, padx = 20, pady = 20)


        # Initiate all of the things
        self.plot_info = None
        self.title_update_frame = None
        self.color_selector = None
        self.column_values = []
        self.column_selector = None
        self.check_button = None
        self.show_axes_check = None
        self.geoimage_frame = None
        self.allow_heatmap = False
        self.heatmap_check = None
        self.heatmap_sliders = None
        self.plot_value_min = 0
        self.plot_value_max = 100
        self.read_file_name = ""


        self.protocol("WM_DELETE_WINDOW", self.on_closing)


    
    def get_file_name(self):
        self.read_file_name = filedialog.askopenfilename(filetypes=[("Shapefile", "*.shp *.zip")])
        self.initiate_graph()

    def initiate_graph(self): 
        self.geometry("1100x600")
        
        self.plot_info = GeoPlotInformation(gdf_data=gpd.read_file(self.read_file_name),
                                            color="cool", 
                                            vmax=100)
        
        self.plot_info.column = list(self.plot_info.gdf_data.columns)[0]
    
        for column_name in self.plot_info.gdf_data.columns:
            try:
                self.plot_info.gdf_data[column_name] = self.plot_info.gdf_data[column_name].astype(float)
            except:
                continue
        
         
        self.title_update_frame = TextFieldEntryFrame(self, 
                                                      frame_label = "Graph Title",
                                                      placeholder_text="Enter Graph Title", 
                                                      button_text="Update Graph Title",
                                                      command = self.update_title)
   
        self.color_selector = ColorDropdownFrame(self, 
                                                 color=self.plot_info.color,
                                                 command=self.switch_color)
        
        self.column_values = list(self.plot_info.gdf_data.columns)
        self.column_values.remove('geometry')
        
       
        self.column_selector = RadialSelectFrame(self, 
                                                 list_name= "Map Display",
                                                 item_list= self.column_values, 
                                                 command=self.update_column,
                                                 width = 200)
        
        self.check_button = ctk.CTkButton(self, text="Print Graphing Info", command=self.print_debug)
        self.show_axes_check = CheckBoxFrame(self, 
                                             check_name = "Show Axes", 
                                             command=self.toggle_axes,
                                             width = 200)
        
        self.geoimage_frame = GeoGraphFrame(self.plot_info, self)
        
        # Heatmap options  
        self.allow_heatmap = False 
        self.plot_value_min = 0
        self.plot_value_max = 100
        self.add_heatmap_items()
        
                
        # Grid Positioning Defaults 
        self.title_update_frame.grid(row=0, column=0, sticky = "ew", pady=5)
        self.color_selector.grid(row=1, column=0, sticky = "ew", pady=5) 
        self.column_selector.grid(row=2, column=0, sticky = "nsew",pady=5)
        self.check_button.grid(row = 6, column = 0, sticky = "ew",pady=5)


        self.show_axes_check.grid(row=0, column=1, sticky = "nsew", padx= 20,pady=5)
       
        self.grid_rowconfigure(2, minsize=150, weight=1)
        self.grid_columnconfigure(2, weight=1)
        
        self.geoimage_frame.grid(row=0, column=2, rowspan=7, sticky="nsew")

        self.update_graph()



    def print_debug(self):
        print(self.plot_info)
    
    def update_title(self):
        self.plot_info.title = self.title_update_frame.get_value()
        self.update_graph()
        
    def switch_color(self, _ = None):
        self.plot_info.color = self.color_selector.get_value()

        if not self.allow_heatmap or self.plot_info.color in ["tab20", "tab20b", "tab20c"]:
            self.plot_info.heat_bar = False
            self.disable_heatmap_items()
            self.update_graph()
            return

        if self.allow_heatmap:
            self.add_heatmap_items()
        else:
            self.disable_heatmap_items()

        self.update_graph()
        



    def add_heatmap_items(self):
        show_heatbar = True
        if self.heatmap_check is not None:
            show_heatbar = self.heatmap_check.get_value()
            
        self.heatmap_check = CheckBoxFrame(self, 
                                           check_name = "Heatmap Bar",
                                           command=self.toggle_heatmap)

        if show_heatbar:
            self.heatmap_check.select()       
        else:
            self.heatmap_check.deselect()

        # self.heatmap_check.select()       

        self.heatmap_sliders = MinMaxSliderFrame(self,
                                                 min_value=self.plot_info.vmin,
                                                 min_value_name="Min Val Heatmap",
                                                 max_value=self.plot_info.vmax,
                                                 max_value_name="Max val Heatmap",
                                                 update_button_name="Update Graph",
                                                 update_button_command=self.update_heat_min_max)
        self.heatmap_sliders.set_from_to(self.plot_value_min,self.plot_value_max)
        self.heatmap_sliders.set(self.plot_info.vmin, self.plot_info.vmax)
        self.heatmap_check.grid(row=1, column=1, sticky = "nsew", padx=20, pady=5)
        self.heatmap_sliders.grid(row=2, column=1, sticky = "new", padx=20, pady=5)
        
        if not self.allow_heatmap:
            self.disable_heatmap_items()
        
            
       
    def toggle_heatmap(self):
        if self.heatmap_check is not None and not self.heatmap_check.get_value():
            self.plot_info.heat_bar = False
        
        else:
            self.plot_info.heat_bar=True
            self.add_heatmap_items()
        # Set the mins here again
        self.update_graph()

    def disable_heatmap_items(self):
        if self.heatmap_check is not None:
            self.heatmap_check.disable()
        if self.heatmap_sliders is not None:
            self.heatmap_sliders.disable()

    def update_column(self):
        self.plot_info.column = self.column_selector.get_checked_item()
        self.plot_info.vmin_max_set = False
        
        # Change these so that they grab the min and max from the given column
        if self.plot_info.gdf_data[self.plot_info.column].dtype == 'float64':
            self.allow_heatmap = True
            
            self.plot_value_min = min(self.plot_info.gdf_data[self.plot_info.column])
            self.plot_info.vmin = self.plot_value_min
            
            self.plot_value_max = max(self.plot_info.gdf_data[self.plot_info.column])
            self.plot_info.vmax = self.plot_value_max
        
        else:
            self.plot_value_min = 0
            self.plot_info.vmin = 0
            self.plot_value_max = 100
            self.plot_info.vmax = 100
            self.allow_heatmap = False
              
        self.switch_color()

    def toggle_axes(self):
        self.plot_info.axes = not self.plot_info.axes
        self.update_graph()
        
    def update_heat_min_max(self):
        self.plot_info.vmin_max_set = True
        self.plot_info.vmin = self.heatmap_sliders.get_min()
        self.plot_info.vmax = self.heatmap_sliders.get_max()
        self.update_graph()
        
    def update_graph(self):
        self.geoimage_frame.update(self.plot_info)
    
    def on_closing(self):
        if self.geoimage_frame is not None and self.geoimage_frame.winfo_exists():
            self.geoimage_frame.destroy()
        
        self.quit()
        self.destroy()

def main():
    app = ShapeFileViewer()
    app.mainloop()

if __name__ == "__main__":
    main()
