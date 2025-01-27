# Usar una imagen base de Node.js
FROM node:14-alpine

# Copiar los archivos al contenedor
COPY server.js ./
COPY application.js ./

# Crear un archivo package.json y agregar las dependencias necesarias
RUN apk add --no-cache curl
RUN npm init -y
RUN npm install express yargs request systeminformation

# Crear un script de inicio para gestionar ambos servicios
COPY start.sh .
RUN chmod +x start.sh

# Exponer el puerto del servidor
EXPOSE 8080

# Ejecutar el script de inicio
CMD ["./start.sh"]

