FROM node:14-alpine


# Copiar los archivos de la aplicación al contenedor
COPY gateway.js device.js ./

# Limpiar el caché de npm y luego instalar las dependencias
RUN apk add --no-cache curl
RUN npm install express request yargs systeminformation

# Expone los puertos que usarán la gateway y el device
EXPOSE 8082

# Crear un script de inicio para gestionar ambos servicios
COPY start.sh .
RUN chmod +x start.sh

# Ejecutar el script de inicio
CMD ["./start.sh"]
