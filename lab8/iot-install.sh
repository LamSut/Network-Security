#!/bin/bash

set -e  # Exit on any error

# Step 1: Update and Upgrade the System
echo "Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Step 2: Install Essential Dependencies
echo "Installing dependencies..."
sudo apt install -y curl wget git build-essential python3 python3-pip nodejs npm openssl ufw mosquitto mosquitto-clients docker.io docker-compose

# Step 3: Set Up the Mosquitto MQTT Broker
echo "Enabling Mosquitto service..."
sudo systemctl enable mosquitto
sudo systemctl start mosquitto

# Step 4: Install Node-RED
echo "Installing Node-RED..."
sudo npm install -g --unsafe-perm node-red

# Step 5: Install ThingsBoard
echo "Installing ThingsBoard..."
wget https://github.com/thingsboard/thingsboard/releases/download/v3.6/thingsboard-3.6.deb
sudo dpkg -i thingsboard-3.6.deb
sudo systemctl enable thingsboard
sudo systemctl start thingsboard

# Step 6: Install InfluxDB
echo "Installing InfluxDB..."
wget -qO- https://repos.influxdata.com/influxdb.key | sudo tee /usr/share/keyrings/influxdb-keyring.asc
source /etc/os-release
echo "deb [signed-by=/usr/share/keyrings/influxdb-keyring.asc] https://repos.influxdata.com/debian $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/influxdb.list
sudo apt update && sudo apt install -y influxdb
sudo systemctl enable influxdb
sudo systemctl start influxdb

# Step 7: Configure the Firewall
echo "Configuring firewall rules..."
sudo ufw allow 1883/tcp  # MQTT
sudo ufw allow 8883/tcp  # MQTT over TLS
sudo ufw allow 5683/udp  # CoAP
sudo ufw allow 8080/tcp  # ThingsBoard Web UI
sudo ufw allow 8086/tcp  # InfluxDB
sudo ufw enable

# Step 8: Verify Installations
echo "Verifying installations..."
mosquitto -v
node -v
npm -v
python3 --version
docker --version
influxd version

# Final Step
echo "IoT setup is complete. Your environment is ready to use."
