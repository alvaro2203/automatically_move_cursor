import pyautogui as screen
import random
import time
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from ttkthemes import ThemedStyle
import threading
from datetime import datetime

screen_width, screen_height = screen.size()

# ------------------------------------- FUNCTIONS -------------------------------------

def write_log(message: str):
    """
    Write a message to the log.

    Parameters:
        message (str): The message to be written to the log.
    """
    log.configure(state="normal")                       # Enable log writing
    log.insert(tk.END, message)
    log.see(tk.END)                                     # Scroll to display the last message
    log.configure(state="disabled")                     # Disable log writing
    
    
def move_cursor():
    """
    Move the cursor to a random position on the screen and click on the taskbar.
    """

    x1 = random.randint(0, screen_width)
    y1 = random.randint(0, screen_height)
    task_bar_x = int(screen_width * 0.8)
    task_bar_y = screen_height - 30
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    try:
        screen.moveTo(x1, y1)
        log_message = f"{timestamp}: Cursor moved to ({screen.position().x}, {screen.position().y})\n"
        screen.click(task_bar_x, task_bar_y)
        write_log(log_message)
        
    except screen.FailSafeException as e:
        print(f"A fail-safe error has occurred: {e}")
        print(f"Recalculating coordinates...")
        move_cursor()
        
        
def move_loop(wait_time: float):
    """
    Continuously move the cursor with a given interval.
    
    Parameters:
        wait_time (float): The interval between cursor movements.
    """

    while not stop_movement_flag.is_set():
        move_cursor()
        time.sleep(wait_time)
    

def start_movement():
    """
    Start cursor movement with user-defined interval.
    """

    interval_str = interval_entry.get()

    try:
        interval = float(interval_str)
        if interval <= 0:
            raise ValueError("The time interval must be a positive number.")

        global stop_movement_flag
        stop_movement_flag = threading.Event()
        write_log("Movement Started.\n")

        movement_thread = threading.Thread(target=move_loop, args=(interval,))
        movement_thread.start()
    
    except ValueError:
        tk.messagebox.showerror("Error", "Please enter a valid numeric value for the time interval.")


def stop_movement_func():
    """
    Stop cursor movement.
    """

    stop_message = "Movement Stopped.\n"
    write_log(stop_message)
    stop_movement_flag.set()
    
    
def on_closing():
    """
    Handle window closing event.
    """
    
    if 'stop_movement_flag' in globals() and not stop_movement_flag.is_set():
        stop_movement_func()                            # Stop movement before closing
        
    app.destroy()                                       # Close App
    
# ------------------------------------- CODE -------------------------------------

app = tk.Tk()
app.title("Cursor Control")

# Configure size and allow resizing
app.geometry("1200x500")                                # Width x Height
app.resizable(True, True)                               # Allow resizing in width and height

# Load icon images
start_icon = tk.PhotoImage(file="./assets/1x/play.png")
stop_icon = tk.PhotoImage(file="./assets/1x/pause.png")

# Apply a different theme to the GUI
style = ThemedStyle(app)
style.set_theme("arc")

# ttk style buttons
style.configure("TButton", padding=(10, 5, 10, 5), font='Helvetica 10')

# Configure grid layout
app.grid_columnconfigure(0, weight=4)
app.grid_columnconfigure(1, weight=6)

# Frame for controls
main_frame = ttk.Frame(app)
main_frame.grid(row=0, column=0, rowspan=4, sticky="nsew", padx=10, pady=10)
main_frame.grid_propagate(False)

# Log area
log = scrolledtext.ScrolledText(app, width=30, height=30, state="disabled")
log.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
log.grid_propagate(False)

# Buttons
start_button = ttk.Button(main_frame, text="Iniciar", image=start_icon, compound=tk.LEFT, command=start_movement, width=15)
start_button.grid(row=1, column=0, pady=10, padx=(5, 5), sticky="ew")

stop_button = ttk.Button(main_frame, text="Detener", image=stop_icon, compound=tk.LEFT, command=stop_movement_func, width=15)
stop_button.grid(row=1, column=1, pady=10, padx=(5, 5), sticky="ew")

# Label and entry for time interval
ttk.Label(main_frame, text="Intervalo de Tiempo (segundos):").grid(row=2, column=0, pady=10)
interval_entry = ttk.Entry(main_frame, width=20)
interval_entry.insert(tk.END, "40")                    
interval_entry.grid(row=2, column=1, pady=10)

# Handle window closing event
app.protocol("WM_DELETE_WINDOW", on_closing)

# Run the GUI
app.mainloop()