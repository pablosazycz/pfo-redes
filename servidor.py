import socket
import sqlite3
from datetime import datetime

# ------------------- Crear o conectar la base de datos -------------------
def crear_bd():
    try:
        conn = sqlite3.connect('chat.db')
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS mensajes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                contenido TEXT NOT NULL,
                fecha_envio TEXT NOT NULL,
                ip_cliente TEXT NOT NULL
            )
        """)
        conn.commit()
        conn.close()
        print("[BD] Base de datos creada o existente.")
    except Exception as e:
        print(f"[ERROR BD] {e}")
        exit()

#  Guardar mensaje en la base de datos 
def guardar_mensaje(contenido, ip_cliente):
    try:
        conn = sqlite3.connect('chat.db')
        cursor = conn.cursor()
        fecha_envio = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("INSERT INTO mensajes (contenido, fecha_envio, ip_cliente) VALUES (?, ?, ?)", (contenido, fecha_envio, ip_cliente))
        conn.commit()
        conn.close()
        return fecha_envio
    except Exception as e:
        print(f"[ERROR GUARDAR MENSAJE] {e}")
        return None

#  Inicializar el socket del servidor 
def inicializar_socket():
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(("localhost", 5000))
        server_socket.listen()
        print("[SOCKET] Servidor escuchando en localhost:5000")
        return server_socket
    except Exception as e:
        print(f"[ERROR SOCKET] {e}")
        exit()

#  Aceptar conexiones y procesar mensajes 
def aceptar_conexiones(server_socket):
    while True:
        conn, addr = server_socket.accept()
        print(f"[CONECTADO] Cliente {addr}")
        try:
            while True:  # 👈 agregado nuevo
                data = conn.recv(1024).decode()
                if not data:  # 👈 si no hay más datos, el cliente se desconectó
                    print(f"[DESCONECTADO] Cliente {addr}")
                    break
                print(f"[MENSAJE] {addr}: {data}")
                timestamp = guardar_mensaje(data, addr[0])
                if timestamp:
                    respuesta = f"Mensaje recibido: {timestamp}"
                else:
                    respuesta = "Error al guardar el mensaje."
                conn.sendall(respuesta.encode())
        except Exception as e:
            print(f"[ERROR RECEPCIÓN] {e}")
        finally:
            conn.close()

#  Programa principal 
if __name__ == "__main__":
    crear_bd()
    servidor = inicializar_socket()
    aceptar_conexiones(servidor)
