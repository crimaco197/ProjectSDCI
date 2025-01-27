# Usar una imagen base de Node.js
FROM node:14-alpine

# Copiar el archivo server.js al contenedor
COPY gateway.js ./

RUN apk add --no-cache curl
RUN npm install express request yargs systeminformation
# Exponer el puerto en el que correrá el servidor
EXPOSE 8081

# Comando para lanzar la gateway y conectarla al servidor ya creado
CMD ["node", "gateway.js", "--local_ip", "0.0.0.0", "--local_port", "8081", "--local_name", "gwi","--remote_ip", "iot-server-clusterip","--remote_port", "8080", "--remote_name","server"]
