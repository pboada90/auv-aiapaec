from customtkinter import *
from PIL import Image

app = CTk()

app.geometry("500x400")

set_appearance_mode("dark")

def forward_speed():
    print("Speed increase 25%")

def backward_speed():
    print("Speed decrease 25%")

btn_fwd_speed = CTkButton(master=app, text="Increase Speed", command=forward_speed)
btn_bwd_speed = CTkButton(master=app, text="Decrease Speed", command=backward_speed)

btn_fwd_speed.place(relx=0.5, rely=0.5, anchor="center")
btn_bwd_speed.place(relx=0.5, rely=0.65, anchor="center")

app.mainloop()