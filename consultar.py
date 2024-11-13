import sqlite3

# Conectar a la base de datos
conn = sqlite3.connect('pesos.db')
cursor = conn.cursor()

# Ejecutar la consulta para ver todos los registros
cursor.execute("SELECT * FROM registros WHERE id = 1")
registros = cursor.fetchall()

# Mostrar los resultados
for registro in registros:
    print(registro)

# Cerrar la conexión
conn.close()