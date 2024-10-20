from customtkinter import *
import joystick_control

try:
    joystick = joystick_control.init_joystick()
    print("Joystick initialized!")
except Exception as e:
    print(e)
    exit()

set_appearance_mode("dark")

class ConnectionFrame(CTkFrame):
    def __init__(self, master, title):
        super().__init__(master)
        #self.grid_columnconfigure(0, weight=1)
        self.title = title

        self.title = CTkLabel(self, text=self.title, fg_color="gray30", corner_radius=6)
        self.title.grid(row=0, column=0, columnspan=2, padx=10, pady=(10, 0), sticky="ew")
        
        self.ip_label = CTkLabel(self, text="IP address:")
        self.ip_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")

        self.ip_entry = CTkEntry(self, placeholder_text="Enter IP address...")
        self.ip_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        self.password_label = CTkLabel(self, text="Password:")
        self.password_label.grid(row=2, column=0, padx=10, pady=10, sticky="e")

        self.password_entry = CTkEntry(self, placeholder_text="Enter password...", show="*")
        self.password_entry.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

        self.button = CTkButton(self, text="Connect to AUV", command=self.button_connection)
        self.button.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

    def get(self):
        ip_address = self.ip_entry.get()
        password = self.password_entry.get()

        return ip_address, password

    def button_connection(self):
        ip_address, password = self.get()
        print(f"Trying to connect to {ip_address} with the password {password}")

class SurgeFrame(CTkFrame):
    def __init__(self, master, title):
        super().__init__(master)
        #self.grid_columnconfigure(0, weight=1)
        self.title = title

        self.title = CTkLabel(self, text=self.title, fg_color="gray30", corner_radius=6)
        self.title.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="ew")

class NavigationFrame(CTkFrame):
    def __init__(self, master, title):
        super().__init__(master)
        #self.grid_columnconfigure(0, weight=1)
        self.title = title

        self.title = CTkLabel(self, text=self.title, fg_color="gray30", corner_radius=6)
        self.title.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="ew")

class TelemetryFrame(CTkFrame):
    def __init__(self, master, title):
        super().__init__(master)
        #self.grid_columnconfigure(0, weight=1)
        self.title = title

        self.title = CTkLabel(self, text=self.title, fg_color="gray30", corner_radius=6)
        self.title.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="ew")

class DepthFrame(CTkFrame):
    def __init__(self, master, title):
        super().__init__(master)
        #self.grid_columnconfigure(0, weight=1)
        self.title = title

        self.title = CTkLabel(self, text=self.title, fg_color="gray30", corner_radius=6)
        self.title.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="ew")

class App(CTk):
    def __init__(self):
        super().__init__()

        self.title("Ground Control - GUI")
        self.geometry("800x500")

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure((1, 2), weight=1)
        #self.grid_rowconfigure((0, 1), weight=1)

        self.connection_frame = ConnectionFrame(self, "Connection to AUV")
        self.connection_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.surge_frame = SurgeFrame(self, "Surge velocity")
        self.surge_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.navigation_frame = NavigationFrame(self, "Navigation direction")
        self.navigation_frame.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

        self.telemetry_frame = TelemetryFrame(self, "Telemetry")
        self.telemetry_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        self.depth_frame = DepthFrame(self, "Depth")
        self.depth_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        self.check_joystick_events()

    def check_joystick_events(self):
        events = joystick_control.get_joystick_events()
        for event in events:
            if event == "QUIT":
                self.exit()

            elif isinstance(event, tuple) and event[0] == "BUTTONDOWN":
                if event[1] == 11:
                    print("Emerging...")
                elif event[1] == 12:
                    print("Inmersing...")

            elif isinstance(event, tuple) and event[0] == "axis_2":
                print(f"{event[0]} value = {event[1]}")

            elif isinstance(event, tuple) and event[0] == "axis_3":
                print(f"{event[0]} value = {event[1]}")
            
            elif isinstance(event, tuple) and event[0] == "BUTTONUP":
                if event[1] == 11:
                    print("Emerging stopped...")
                elif event[1] == 12:
                    print("Inmersing stopped...")

        self.after(100, self.check_joystick_events)

app = App()

app.mainloop()