import tkinter
import gpustat
import threading
import time
import os
IS_BUSY = False
SPINNERS = ["-","/","|","\\"]


root = tkinter.Tk()
main_window = tkinter.Toplevel()
main_window.overrideredirect(True)
button_photo = tkinter.PhotoImage(file="")
photo = button_photo.subsample(8,8)



def set_loading_button():
    global IS_BUSY
    while IS_BUSY:
        for spinner in SPINNERS:

            check_temp_button.configure(text=f"[{spinner}] loading...")
            time.sleep(0.2)

    check_temp_button.configure(text="Check Temp")

def check_temperature_command():
    global IS_BUSY
    if IS_BUSY:
        return
    IS_BUSY = True
    t = threading.Thread(target=check_temperature)
    t0 = threading.Thread(target=set_loading_button)

    t.start()
    t0.start()


def check_temperature():
    global IS_BUSY
    time.sleep(1)
    stats = gpustat.GPUStatCollection.new_query()
    temp_textbox.configure(state="normal")
    temp_textbox.delete(0,tkinter.END)
    temp_textbox.insert(0,f"{stats.gpus[0].temperature}°")
    temp_textbox.configure(state="readonly")
    IS_BUSY = False

def exit_program():
    root.quit()
    quit()

def make_draggable(widget):
    widget.bind("<Button-1>", on_drag_start)
    widget.bind("<B1-Motion>", on_drag_motion)

def on_drag_start(event):
    global main_window
    widget = main_window
    widget._drag_start_x = event.x
    widget._drag_start_y = event.y

def on_drag_motion(event):
    global main_window
    widget = main_window
    x = widget.winfo_x() - widget._drag_start_x + event.x
    y = widget.winfo_y() - widget._drag_start_y + event.y
    widget.geometry(f'400x250+{x}+{y}')

def on_map(e):
    global main_window, root
    main_window.wm_deiconify()

def on_un_map(e):
    global main_window, root
    main_window.wm_withdraw()

def setup_main_window():
    global main_window, root
    root.bind('<Unmap>', on_un_map)
    root.bind('<Map>', on_map)
    root.wm_withdraw()
    main_window['background'] = 'black'
    
    ws = root.winfo_screenwidth() 
   
    hs = root.winfo_screenheight()
    main_window.geometry(f"400x250")

setup_main_window()
make_draggable(main_window)

title_label = tkinter.Label(main_window,text="Lizard",foreground="red",background="black",font=("Segoe UI Light",16))
title_label.grid(column=0,row=1,padx=10)

button_border = tkinter.Frame(main_window,background="red",)
button = tkinter.Button(button_border,text="Exit",fg="red",background="black",command=exit_program)
button.pack(fill="both",expand=True,padx=1,pady=1)
button_border.grid(padx=270,pady=10,column=1,row=1)


button_check_temp_border = tkinter.Frame(main_window,background="red",)
check_temp_button = tkinter.Button(button_check_temp_border,text="Check Temp",background="black",foreground="red",command=check_temperature_command)
check_temp_button.pack(fill="both",expand=True,padx=1,pady=1)
button_check_temp_border.place(x=160,y=75)


temp_textbox = tkinter.Entry(main_window,width=25,state="readonly")
temp_textbox.place(x=125,y=110)
root.iconbitmap("Assets\\Lightining.ico")
root.mainloop()