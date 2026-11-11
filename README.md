# Chat TCP con Python, hilos y Docker

Aplicación de chat para tres participantes: un servidor y dos clientes. El
servidor corre en un contenedor Docker; cada cliente corre con Python en una
terminal independiente. Los mensajes se envían a todos los participantes y
pueden escribirse al mismo tiempo.

## Requisitos

- Docker Desktop con Docker Compose.
- Python 3 en la computadora para ejecutar los clientes.

## Iniciar el servidor

Abre una terminal de VS Code en esta carpeta y ejecuta:

```powershell
docker compose up --build -d
```

El servidor queda escuchando en el puerto `5000`. Para escribir desde el
servidor, abre otra terminal de VS Code en esta carpeta y adjúntate al servicio:

```powershell
docker compose attach servidor
```

Dale a ENTER primero, y cuando aparezca el prompt `[SERVIDOR]:`, escribe el mensaje y presiona Enter de nuevo para enviarlo.
Los mensajes que escriban los clientes también aparecerán en esa terminal.
Presiona `Ctrl+C` desde la terminal adjunta para detener el servidor.

## Conectar los dos clientes

Abre otras dos terminales de VS Code, también ubicadas en esta carpeta. En la
segunda terminal ejecuta el Cliente 1 y en la tercera el Cliente 2:

```powershell
python cliente1.py
```

```powershell
python cliente2.py
```

Cada archivo se identifica ante el servidor como `CLIENTE 1` o `CLIENTE 2`, sin
importar cuál se conecte primero. Escribe un mensaje y presiona Enter; el otro
cliente lo recibe y el servidor lo muestra en su terminal. El mensaje no se
reenvía al cliente que lo escribió para evitar que aparezca duplicado. Para
salir de un cliente, escribe `/salir`.

## Cómo se comunican

1. Docker Compose construye la imagen con el `Dockerfile` e inicia `servidor.py`
   dentro del contenedor.
2. El servidor escucha en `0.0.0.0:5000`, lo que permite recibir conexiones por
   la interfaz de red del contenedor. Compose publica el puerto como
   `5000:5000`: el puerto `5000` de la computadora anfitriona se conecta con el
   puerto `5000` del contenedor.
3. `cliente1.py` y `cliente2.py` usan TCP y se conectan a `127.0.0.1:5000` en
   la computadora anfitriona. Docker reenvía esas conexiones al servidor del
   contenedor.
4. Cada archivo de cliente envía su nombre como primera línea. El servidor
   valida e identifica a los participantes, y crea un hilo para cada conexión.
   En cada cliente, otro hilo recibe mensajes mientras el hilo principal espera
   lo que escriba el usuario.
5. Los mensajes viajan como líneas de texto UTF-8 terminadas en salto de línea.
   El servidor añade el nombre del participante y los difunde a los clientes.

Los clientes se ejecutan en la computadora anfitriona, no dentro de Docker.
Por eso se conectan a `127.0.0.1`; `0.0.0.0` es la dirección en la que escucha el
servidor, no la dirección que se configura en el cliente.

## Archivos

- `servidor.py`: acepta dos conexiones concurrentes, identifica a los clientes
  y distribuye los mensajes.
- `cliente1.py`: conecta como `CLIENTE 1`, envía texto y recibe mensajes en
  paralelo.
- `cliente2.py`: conecta como `CLIENTE 2`, envía texto y recibe mensajes en
  paralelo.
- `Dockerfile`: crea la imagen Python del servidor.
- `compose.yaml`: publica el puerto del servidor y permite escribir en su
  terminal.
