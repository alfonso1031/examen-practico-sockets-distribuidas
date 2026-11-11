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

El servidor queda escuchando en el puerto `5000` en segundo plano. Para escribir
desde el servidor, abre otra terminal de VS Code en esta carpeta y adjúntate al
servicio:

```powershell
docker compose attach servidor
```

En la terminal adjunta escribe junto al prompt `[SERVIDOR]:`; el texto se ve
mientras escribes. Usa solo esta terminal interactiva para escribir mensajes.
Enter vacío no envía ningún mensaje y deja listo el siguiente prompt. Los
mensajes de los clientes también aparecerán con sus etiquetas en esa terminal.
Si llega un mensaje mientras escribes, aparecerá en otra línea y se mostrará de
nuevo el prompt del servidor.
Para detener el servidor, ejecuta `docker compose down` en otra terminal.

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
importar cuál se conecte primero. El prompt de cada terminal muestra su nombre.
Los Enter vacíos se ignoran. El otro cliente recibe cada mensaje y el servidor
lo muestra en su terminal. El emisor ya ve su mensaje en su propio terminal, así
que el servidor no se lo reenvía. Para salir de un cliente, escribe `/salir`.
