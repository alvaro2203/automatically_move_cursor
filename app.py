import pyautogui as screen
import random
import time
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from ttkthemes import ThemedStyle
import threading
from datetime import datetime

x, y = screen.size()
selected_area = None

# ------------------------------------- FUNCTIONS -------------------------------------

def write_log(message):
    log.configure(state="normal")                       # Habilitar la escritura
    log.insert(tk.END, message)
    log.see(tk.END)                                     # Desplazar el scroll para mostrar el último mensaje
    log.configure(state="disabled")                     # Deshabilitar la escritura
    
    
def move_cursor():
    x1 = random.randint(0, x)
    y1 = random.randint(0, y)
    barra_tareas_x = int(x / 1)                         # Coordenada X de la barra de tareas (puedes ajustarla según tu configuración)
    barra_tareas_y = y - 30                             # Coordenada Y de la barra de tareas (30 píxeles desde la parte inferior)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    try:
        screen.moveTo(x1, y1)
        log_message = f"{timestamp}: Cursor moved to ({screen.position().x}, {screen.position().y})\n"
        screen.click(barra_tareas_x, barra_tareas_y)
        print(log_message)
        write_log(log_message)
        
    except screen.FailSafeException as e:
        print(f"A fail-safe error has occurred: {e}")
        print(f"Recalculating coordinates...")
        move_cursor()
        
        
def move_loop(wait_time: float):
    while not stop_movement_flag.is_set():
        move_cursor()
        time.sleep(wait_time)


# Función para iniciar el movimiento con los valores ajustados por el usuario
def start_with_values():
    interval_str = interval_entry.get()
    
    try:
        interval = float(interval_str)
        if interval <= 0:
            raise ValueError("El intervalo de tiempo debe ser un número positivo.")
        start_movement(interval)
    
    except ValueError:
        tk.messagebox.showerror("Error", "Por favor, introduce un valor númerico válido para el intervalo de tiempo.")
        

def start_movement(interval: float):
    global stop_movement_flag
    stop_movement_flag = threading.Event()

    start_message = "Movement Started.\n"
    print(start_message)
    write_log(start_message)

    movement_thread = threading.Thread(target=move_loop, args=(interval,))
    movement_thread.start()


def stop_movement_func():
    stop_message = "Movement Stopped.\n"
    print(stop_message)
    write_log(stop_message)
    stop_movement_flag.set()
    
    
def on_closing():
    if 'stop_movement_flag' in globals() and not stop_movement_flag.is_set():
        stop_movement_func()                            # Detener el movimiento antes de cerrar
        
    app.destroy()                                       # Cerrar la aplicación
    
# ------------------------------------- CODE -------------------------------------

# Crear la interfaz gráfica
app = tk.Tk()
app.title("Control de Cursor")

# Configurar el tamaño y permitir redimensionamiento
app.geometry("1200x500")                                # Ancho x Alto
app.resizable(True, True)                               # Permitir redimensionar en ancho y alto

# Cargar imágenes de los iconos
start_icon = tk.PhotoImage(file="./assets/1x/play.png")
stop_icon = tk.PhotoImage(file="./assets/1x/pause.png")

# Aplicar un tema diferente a la interfaz gráfica
style = ThemedStyle(app)
style.set_theme("arc")  # Tema "arc", puedes elegir otro si prefieres

# Estilo para botones ttk
style.configure("TButton", padding=(10, 5, 10, 5), font='Helvetica 10')

# Configure the grid layout
app.grid_columnconfigure(0, weight=4)
app.grid_columnconfigure(1, weight=6)

# Marco para los controles
main_frame = ttk.Frame(app)
main_frame.grid(row=0, column=0, rowspan=4, sticky="nsew", padx=10, pady=10)
main_frame.grid_propagate(False)

# Log de movimientos
log = scrolledtext.ScrolledText(app, width=30, height=30, state="disabled")
log.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
log.grid_propagate(False)

# Botones
boton_iniciar = ttk.Button(main_frame, text="Iniciar", image=start_icon, compound=tk.LEFT, command=start_with_values, width=15)
boton_iniciar.grid(row=1, column=0, pady=10, padx=(5, 5), sticky="ew")

boton_detener = ttk.Button(main_frame, text="Detener", image=stop_icon, compound=tk.LEFT, command=stop_movement_func, width=15)
boton_detener.grid(row=1, column=1, pady=10, padx=(5, 5), sticky="ew")

# Etiquetas y controles para ajustar el intervalo de tiempo
ttk.Label(main_frame, text="Intervalo de Tiempo (segundos):").grid(row=2, column=0, pady=10)
interval_entry = ttk.Entry(main_frame, width=20)
interval_entry.insert(tk.END, "40")                    
interval_entry.grid(row=2, column=1, pady=10)

# Configurar la función que se ejecutará al cerrar la ventana
app.protocol("WM_DELETE_WINDOW", on_closing)

# Ejecutar la interfaz gráfica
app.mainloop()