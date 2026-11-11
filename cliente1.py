import socket
import threading


# identifica este archivo como el cliente uno ante el servidor
NOMBRE = "CLIENTE 1"
HOST = "127.0.0.1"
PORT = 5000

# crea el socket y se conecta al puerto publicado por docker
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect((HOST, PORT))

# envia el nombre como primera linea para que el servidor lo identifique
cliente.sendall((NOMBRE + "\n").encode("utf-8"))

print(f"Conectado al servidor como {NOMBRE}")


def recibir_mensajes():
    # lee mensajes completos mientras el usuario escribe en esta terminal
    canal = cliente.makefile("r", encoding="utf-8")
    for linea in canal:
        print("\n" + linea.rstrip())


# el hilo receptor permite ver mensajes sin esperar a que el usuario escriba
threading.Thread(target=recibir_mensajes, daemon=True).start()

try:
    while True:
        # el prompt muestra quien esta escribiendo
        mensaje = input(f"[{NOMBRE}]: ")

        # ignora enter vacio para no enviar mensajes en blanco
        if not mensaje.strip():
            continue

        # envia la orden de salida y termina el ciclo del cliente
        if mensaje.lower() == "/salir":
            cliente.sendall((mensaje + "\n").encode("utf-8"))
            break

        # el salto de linea separa este mensaje del siguiente en el servidor
        cliente.sendall((mensaje + "\n").encode("utf-8"))
except (EOFError, KeyboardInterrupt):
    # cierra el cliente si se termina la entrada o se presiona ctrl c
    print("\nCliente desconectado")
finally:
    # libera el socket del cliente al salir
    cliente.close()
