#!/bin/sh

# Inicia el servidor en segundo plano
node server.js --local_ip 0.0.0.0 --local_port 8080 --local_name server &

# Inicia una instancia de la aplicación en primer plano
node application.js --remote_ip 127.0.0.1 --remote_port 8080 --device_name dev1 --send_period 5000
