# usa una imagen ligera con python
FROM python:3.12-slim

# establece la carpeta de trabajo dentro del contenedor
WORKDIR /app

# copia el programa servidor a la imagen
COPY servidor.py .

# documenta el puerto que usa el servidor
EXPOSE 5000

# inicia el servidor al ejecutar el contenedor
CMD ["python", "-u", "servidor.py"]
