import socket
import threading


# este archivo se conecta con el nombre de cliente 2
NOMBRE = "CLIENTE 2"
HOST = "127.0.0.1"
PORT = 5000

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect((HOST, PORT))
cliente.sendall((NOMBRE + "\n").encode("utf-8"))

print(f"Conectado al servidor como {NOMBRE}")


def recibir_mensajes():
    canal = cliente.makefile("r", encoding="utf-8")
    for linea in canal:
        print("\n" + linea.rstrip())


threading.Thread(target=recibir_mensajes, daemon=True).start()

try:
    while True:
        mensaje = input(f"[{NOMBRE}]: ")
        if mensaje.lower() == "/salir":
            cliente.sendall((mensaje + "\n").encode("utf-8"))
            break
        cliente.sendall((mensaje + "\n").encode("utf-8"))
except (EOFError, KeyboardInterrupt):
    print("\nCliente desconectado")
finally:
    cliente.close()
