import socket
import threading


HOST = "0.0.0.0"
PORT = 5000

clientes = {}
candado = threading.Lock()
servidor = None


def enviar_a_todos(mensaje, emisor=None):
    # envia un mensaje a todos los clientes conectados
    with candado:
        for conexion in list(clientes):
            if conexion == emisor:
                continue
            try:
                conexion.sendall((mensaje + "\n").encode("utf-8"))
            except OSError:
                pass


def atender_cliente(conexion):
    # recibe mensajes de un cliente y los comparte con los demas
    canal = conexion.makefile("r", encoding="utf-8")
    nombre = canal.readline().strip()

    with candado:
        nombre_en_uso = nombre in clientes.values()
        nombre_valido = nombre in ("CLIENTE 1", "CLIENTE 2")
        if nombre_valido and not nombre_en_uso:
            clientes[conexion] = nombre

    if not nombre_valido or nombre_en_uso:
        conexion.sendall(
            "[SERVIDOR]: El nombre no es valido o ya esta conectado\n".encode("utf-8")
        )
        canal.close()
        conexion.close()
        return

    for linea in canal:
        mensaje = linea.strip()
        if not mensaje:
            continue
        if mensaje.lower() == "/salir":
            break

        texto = f"[{nombre}]: {mensaje}"
        print(texto, flush=True)
        enviar_a_todos(texto, emisor=conexion)

    canal.close()
    conexion.close()

    with candado:
        clientes.pop(conexion, None)

def aceptar_clientes():
    # acepta conexiones y crea un hilo para cada cliente
    while True:
        try:
            conexion, _ = servidor.accept()
        except OSError:
            break

        hilo = threading.Thread(
            target=atender_cliente,
            args=(conexion,),
            daemon=True,
        )
        hilo.start()


def main():
    global servidor

    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    servidor.bind((HOST, PORT))
    servidor.listen()

    print(f"[SERVIDOR]: Escuchando en {HOST}:{PORT}", flush=True)
    threading.Thread(target=aceptar_clientes, daemon=True).start()

    try:
        while True:
            mensaje = input("[SERVIDOR]: ")
            if mensaje.strip():
                enviar_a_todos(f"[SERVIDOR]: {mensaje}")
    except (EOFError, KeyboardInterrupt):
        print("\n[SERVIDOR]: Cerrando el chat", flush=True)
    finally:
        servidor.close()


if __name__ == "__main__":
    main()
