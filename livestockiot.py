import paho.mqtt.client as mqtt
import random
import time
import json

# ThingsBoard MQTT server details
THINGSBOARD_HOST = "thingsboard.cloud"
ACCESS_TOKEN = "JunbdZxWKRqQIMIMXouy"  # Replace with your device token

# MQTT client setup
client = mqtt.Client()
client.username_pw_set(ACCESS_TOKEN)

# Callback for successful connection
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to ThingsBoard successfully!")
    else:
        print("Failed to connect, return code %d\n" % rc)

# Callback for publishing data
def on_publish(client, userdata, mid):
    print("Data published successfully!")

# Set callbacks
client.on_connect = on_connect
client.on_publish = on_publish

# Function to connect to ThingsBoard
def connect_to_thingsboard():
    print("Connecting to ThingsBoard...")
    try:
        client.connect(THINGSBOARD_HOST, 1883, 60)
        client.loop_start()  # Start the MQTT loop in a separate thread
        print("Connected!")
    except Exception as e:
        print(f"Connection failed: {e}")
        exit()

# Function to simulate livestock health data
def generate_data():
    temperature = round(random.uniform(37.5, 40.5), 1)  # Simulated temperature
    heart_rate = random.randint(60, 100)  # Simulated heart rate
    latitude = round(35.000 + random.uniform(-0.01, 0.01), 6)  # Simulated latitude
    longitude = round(-120.000 + random.uniform(-0.01, 0.01), 6)  # Simulated longitude
    return {
        "temperature": temperature,
        "heartRate": heart_rate,
        "latitude": latitude,
        "longitude": longitude
    }

# Main program
if __name__ == "__main__":
    print("Starting script...")
    connect_to_thingsboard()
    print("Connection established. Starting data transmission...")
    try:
        while True:
            # Generate random livestock data
            data = generate_data()
            payload = json.dumps(data)  # Convert dictionary to JSON
            print("Publishing data:", payload)

            # Publish data to ThingsBoard
            client.publish("v1/devices/me/telemetry", payload)
            time.sleep(5)  # Send data every 5 seconds
    except KeyboardInterrupt:
        print("Program stopped!")
        client.loop_stop()  # Stop the MQTT loop
        client.disconnect()
