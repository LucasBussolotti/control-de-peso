import serial
import sqlite3
import time

# Configuración de la balanza
PORT = 'COM3'  # Cambia 'COM3' por el puerto correcto en tu computadora
BAUDRATE = 9600  # Velocidad común para balanzas, verifica con el manual de la balanza

# Configuración de la base de datos
DB_NAME = 'pesos.db'

# Conexión a la base de datos y creación de la tabla si no existe
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

# Función para guardar el peso en la base de datos
def guardar_peso(peso):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO registros (peso, timestamp) VALUES (?, ?)", (peso, time.strftime('%Y-%m-%d %H:%M:%S')))
    conn.commit()
    conn.close()

# Configuración de la comunicación con la balanza
def leer_peso():
    with serial.Serial(PORT, BAUDRATE, timeout=1) as ser:
        while True:
            try:
                # Lee el peso de la balanza
                peso_bruto = ser.readline().decode('utf-8').strip()
                # Convertir el peso a formato numérico si es válido
                peso = float(peso_bruto)
                
                print(f'Peso leído: {peso} g')
                
                # Guardar el peso en la base de datos
                guardar_peso(peso)
                
                # Espera un intervalo antes de leer el siguiente dato
                time.sleep(1)

            except ValueError:
                print("Error de lectura, intentando de nuevo...")
                continue
            except KeyboardInterrupt:
                print("Programa interrumpido por el usuario.")
                break

if __name__ == '__main__':
    # Inicializar la base de datos
    init_db()
    
    # Iniciar la lectura de datos
    print("Iniciando lectura de la balanza...")
    leer_peso()
