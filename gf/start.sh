#!/bin/sh
# La gateway final SIEMPRE se conecta a la gateway intermediare
# El nombre gwi y el puerto 8081 debe coincidir con el nombre y puerto puesto en el dockerfile de la gateway intermediare
GW_NAME=${GW_NAME:-gw_default}
DEV_NAME=${DEV_NAME:-dev_default}
node gateway.js --local_ip "0.0.0.0" --local_port 8082 --local_name "$GW_NAME" --remote_ip "iot-gateway-clusterip" --remote_port 8081 --remote_name "gwi" &

until nc -z localhost 8082; do
    sleep 1
done
echo "zone gateway ready"

node device.js --local_ip "127.0.0.1" --local_port 9001 --local_name "$DEV_NAME" --remote_ip "127.0.0.1" --remote_port 8082 --remote_name "$GW_NAME" --send_period 3000 &
wait