import socket

#  Inicializar conexión 
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect(("localhost", 5000))
print("[CLIENTE] Conectado al servidor.")

#  Enviar mensajes 
while True:
    mensaje = input("Escribí un mensaje (o 'exit' para salir): ")
    if mensaje.lower() == "exit":
        break

    try:
        cliente.sendall(mensaje.encode())
        respuesta = cliente.recv(1024).decode()
        print("[RESPUESTA DEL SERVIDOR]", respuesta)
    except Exception as e:
        print(f"[ERROR CLIENTE] {e}")
        break

#  Cerrar conexión 
cliente.close()
print("Conexión cerrada.")
