import sqlite3
import tkinter as tk
from tkinter import ttk
import random
from datetime import datetime

# Configuración de la base de datos
DB_NAME = 'pesos.db'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS registros (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        peso REAL,
                        timestamp TEXT
                      )''')
    conn.commit()
    conn.close()

def guardar_peso(peso):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO registros (peso, timestamp) VALUES (?, ?)", (peso, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

def obtener_pesos():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM registros")
    registros = cursor.fetchall()
    conn.close()
    return registros

def agregar_peso_simulado():
    peso_simulado = random.uniform(1000, 2000)
    guardar_peso(peso_simulado)
    actualizar_tabla()
    print(f"Peso simulado guardado: {peso_simulado:.2f} g")

def actualizar_tabla():
    for row in tabla.get_children():
        tabla.delete(row)
    registros = obtener_pesos()
    for registro in registros:
        tabla.insert("", "end", values=(registro[0], f"{registro[1]:.2f} g", registro[2]))

# Inicializar la base de datos
init_db()

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Control de peso producto terminado")
ventana.geometry("768x1024")

# Agregar una etiqueta de texto debajo del título
etiqueta_info = tk.Label(ventana, text="""Este formulario debe completarse cada 15 minutos mientras la producción esté activa.
Los límites máximos y mínimos para cada presentación son los siguientes:
Frascos de 250 gr: 249 - 251 gr
Frascos de 360 gr: 359 - 361 gr
Frascos de 369 gr:  368 - 370 gr
Frascos de 370 gr:  369 - 371 gr
Frascos de 450 gr: 449 - 451 gr
Frascos de 500 gr: 499 - 501 gr
Frascos de 1 kg: 999 - 1001 gr
Baldes de 4 kg: 3.99 - 4.01 kg
Baldes de OTP 4.08 kg = 9 lb:  4.07 - 4.09 kg
Baldes de OTP 21.77 kg = 48 lb: 21.76 - 21.78 kg""", font=("Arial", 10))
etiqueta_info.pack(pady=(10, 0))  # Espacio superior de 10 para separar el título y la etiqueta


# Crear el marco y la tabla para mostrar los registros
frame = ttk.Frame(ventana)
frame.pack(pady=20)

# Tabla para mostrar los registros
tabla = ttk.Treeview(frame, columns=("ID", "Peso", "Fecha y Hora"), show="headings")
tabla.heading("ID", text="ID")
tabla.heading("Peso", text="Peso")
tabla.heading("Fecha y Hora", text="Fecha y Hora")
tabla.pack()

# Botón para agregar peso simulado
boton_agregar = ttk.Button(ventana, text="Agregar Peso Simulado", command=agregar_peso_simulado)
boton_agregar.pack(pady=10)

# Actualizar la tabla con los datos iniciales
actualizar_tabla()

# Ejecutar la aplicación
ventana.mainloop()
