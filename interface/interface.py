import pytz
import tkinter as tk
from tkinter import ttk, Tk, OptionMenu, StringVar
from tkinter import Entry, Label, messagebox
from app.app import App
from errors import *
from schemas.cities import *

class SunriseSunsetApp(Tk):
    def __init__(self):
        super().__init__()
        self.geometry("500x200")
        self.config(padx=100,pady=50)
        self.title("Sunrise/Sunset Graph Generator")
       
        # Create label for start date
        self.start_date_label = Label(self, text="Start Date (MM-DD-YYYY)")
        self.start_date_label.grid(row=0, column=0)
       
        # Create entry for start date
        self.start_date_entry = Entry(self)
        self.start_date_entry.grid(row=0, column=1)
       
        # Create label for end date
        self.end_date_label = Label(self, text="End Date (MM-DD-YYYY)")
        self.end_date_label.grid(row=1, column=0)
       
        # Create entry for end date
        self.end_date_entry = Entry(self)
        self.end_date_entry.grid(row=1, column=1)
    
        # Create label for address
        self.address = Label(self, text="Type your address")
        self.address.grid(row=2, column=0)
        # Create entry for address
        self.address_entry = Entry(self)
        self.address_entry.grid(row=2, column=1)
        
        # Create select button for timezone
        self.timezone_drop = Label(self, text="Timezone")
        self.timezone_drop.grid(row=4, column=0)
        
        self.timezone_var = StringVar()
        self.timezone_var.set('America/Sao_Paulo')
        self.drop = OptionMenu(self, self.timezone_var, *list(pytz.all_timezones))
        self.drop.grid(row=4, column=1)

        # Create button to load data
        self.load_data_button = tk.Button(self, text="Load Data", 
                                    command=self.load_data)
        self.load_data_button.grid(row=5, column=0, columnspan=2, pady=10)

         
    def load_data(self):
        try:
            # Create progress bar
            pb = ttk.Progressbar(
                        self,
                        orient='horizontal',
                        mode='indeterminate',
                        length=280
                )
            pb.grid(column=0, row=5, columnspan=2, padx=10, pady=20)
            self.remove_load_button()
            self.start_progress_bar(pb)
            city = City(
                address = self.address_entry.get()
            )
            download_thread  = App(
                start_dt = self.start_date_entry.get(), 
                end_dt = self.end_date_entry.get(), 
                lat = city.latitude, 
                lng = city.longitude, 
                name_time_zone = self.timezone_var.get()
                )
            download_thread.start()
            self.monitor(download_thread,pb=pb)
        except EndDateFormatException as ex:
            self.generate_error_message(ex,pb)
            self.add_load_button()  
        except StartDateFormatException as ex:
            self.generate_error_message(ex,pb)
            self.add_load_button()  
        except LocationNotFoundException as ex:
            self.generate_error_message(ex,pb)  
            self.add_load_button()  
        finally:
            self.start_date_entry.delete(0, 'end')
            self.end_date_entry.delete(0, 'end')
            self.address_entry.delete(0, 'end')
              
    def start_progress_bar(self,pb):
        pb.start()
    def stop_progress_bar(self,pb):
        pb.stop()
    def remove_progress_bar(self,pb):
        pb.grid_remove()
    def generate_error_message(self, ex,pb)->str:
        error_msg = 'Ops... it seems like you are typing something wrong ☹\n'
        error_msg += str(ex)
        error_msg += "Let's try one more time \n😊"
        self.stop_progress_bar(pb)
        self.remove_progress_bar(pb)
        messagebox.showerror("showerror", error_msg)
    def monitor(self, download_thread, pb):
        """ Monitor the download thread """
        if download_thread.is_alive():
            self.after(5000, lambda: self.monitor(download_thread,pb=pb))
        else:
            self.stop_progress_bar(pb)
            self.remove_progress_bar(pb)
            self.add_load_button()  
            download_thread.generate_matplotlib_graph(download_thread.df_time_and_date)  
    def add_load_button(self):
        self.load_data_button.grid(row=5, column=0, columnspan=2, pady=10)
    def remove_load_button(self):
        self.load_data_button.grid_remove()
        
       

if __name__ == "__main__":
    app = SunriseSunsetApp()
    app.mainloop()
    
