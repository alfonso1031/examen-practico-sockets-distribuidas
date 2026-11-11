import socket
import threading


# escucha conexiones desde docker y desde la computadora
HOST = "0.0.0.0"
PORT = 5000
# guarda las conexiones activas con el nombre de cada cliente
clientes = {}
# protege la lista de clientes cuando trabajan varios hilos
candado = threading.Lock()
# coordina los mensajes que se muestran en la terminal
terminal = threading.Lock()
# indica si el servidor esta esperando que escriban un mensaje
esperando_entrada = False


def mostrar(mensaje):
    # separa cada mensaje del prompt del servidor
    global esperando_entrada
    with terminal:
        if esperando_entrada:
            # deja el mensaje en una linea y vuelve a mostrar el prompt
            print(f"\n{mensaje}\n[SERVIDOR]: ", end="", flush=True)
        else:
            print(mensaje, flush=True)


def enviar(mensaje, emisor=None):
    # envia el mensaje a los clientes conectados
    with candado:
        for cliente in clientes:
            if cliente != emisor:
                try:
                    cliente.sendall((mensaje + "\n").encode("utf-8"))
                except OSError:
                    pass


def atender(conexion):
    # lee el nombre que el cliente envia al conectarse
    canal = conexion.makefile("r", encoding="utf-8")
    nombre = canal.readline().strip()
    with candado:
        clientes[conexion] = nombre

    # recibe mensajes hasta que el cliente se desconecta
    for linea in canal:
        mensaje = linea.strip()
        if mensaje.lower() == "/salir":
            break
        if mensaje:
            # agrega el nombre del cliente antes de compartir el mensaje
            texto = f"[{nombre}]: {mensaje}"
            mostrar(texto)
            enviar(texto, conexion)

    # cierra la conexion y quita al cliente de la lista
    canal.close()
    conexion.close()
    with candado:
        clientes.pop(conexion, None)


def aceptar():
    # atiende cada cliente en un hilo separado
    while True:
        try:
            conexion, _ = servidor.accept()
        except OSError:
            break
        threading.Thread(target=atender, args=(conexion,), daemon=True).start()


def main():
    # configura el socket del servidor
    global servidor, esperando_entrada
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    servidor.bind((HOST, PORT))
    servidor.listen()
    print(f"[SERVIDOR]: Escuchando en {HOST}:{PORT}", flush=True)
    # acepta clientes mientras la terminal permite enviar mensajes
    threading.Thread(target=aceptar, daemon=True).start()

    try:
        while True:
            # muestra el prompt y lee un mensaje escrito desde docker compose
            with terminal:
                esperando_entrada = True
                print("[SERVIDOR]: ", end="", flush=True)
            mensaje = input()
            with terminal:
                esperando_entrada = False
            if mensaje.strip():
                # comparte el mensaje del servidor con los clientes
                enviar(f"[SERVIDOR]: {mensaje}")
    except (EOFError, KeyboardInterrupt):
        print("\n[SERVIDOR]: Cerrando el chat", flush=True)
    finally:
        servidor.close()


if __name__ == "__main__":
    main()
