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
