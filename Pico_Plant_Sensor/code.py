# PlantMonitor Pico
# By Brian McPhail


import time, board, busio, digitalio, os, json # type: ignore
from adafruit_seesaw.seesaw import Seesaw # type: ignore
import wifi, ipaddress, socketpool # type: ignore
import adafruit_minimqtt.adafruit_minimqtt as MQTT # type: ignore
import adafruit_connection_manager # type: ignore

# Get WiFi details, ensure these are setup in settings.toml
ssid = os.getenv("CIRCUITPY_WIFI_SSID")
ssid_password = os.getenv("CIRCUITPY_WIFI_PASSWORD")
mqtt_topic = os.getenv("MQTT_TOPIC")
mqtt_username = os.getenv("MQTT_USERNAME")
mqtt_password = os.getenv("MQTT_PASSWORD")
mqtt_broker = "192.168.50.100"  # Set your MQTT broker address here
device_id = os.getenv("DEVICE_ID")
plant_name = os.getenv("PLANT_NAME")
firmware_version = "0.1"

# Set up the onboard LED (GP25 on standard Pico)
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

# Set up i2c bus
i2c_bus = busio.I2C(scl=board.GP5, sda=board.GP4)

# Initialize soil sensor (s.s)
ss = Seesaw(i2c_bus, addr=0x36)

if None in [ssid, ssid_password, mqtt_topic, mqtt_username, mqtt_password, plant_name]:
    raise RuntimeError("Missing required value in settings.toml")

print()
print("Connecting to WiFi")

#  connect to your SSID
try:
    wifi.radio.connect(ssid, ssid_password)
except TypeError:
    print("Could not find WiFi info. Check your settings.toml file!")
    raise

print("Connected to WiFi")

pool = socketpool.SocketPool(wifi.radio)

#  prints MAC address to REPL
print("My MAC addr:", [hex(i) for i in wifi.radio.mac_address])

#  prints IP address to REPL
print(f"My IP address is {wifi.radio.ipv4_address}")

# Define callback methods which are called when events occur
def connect(mqtt_client, userdata, flags, rc):
    # This function will be called when the mqtt_client is connected
    # successfully to the broker.
    print("Connected to MQTT Broker!")
    print(f"Flags: {flags}\n RC: {rc}")


def disconnect(mqtt_client, userdata, rc):
    # This method is called when the mqtt_client disconnects
    # from the broker.
    print("Disconnected from MQTT Broker!")


def subscribe(mqtt_client, userdata, topic, granted_qos):
    # This method is called when the mqtt_client subscribes to a new feed.
    print(f"Subscribed to {topic} with QOS level {granted_qos}")


def unsubscribe(mqtt_client, userdata, topic, pid):
    # This method is called when the mqtt_client unsubscribes from a feed.
    print(f"Unsubscribed from {topic} with PID {pid}")


def publish(mqtt_client, userdata, topic, pid):
    # This method is called when the mqtt_client publishes data to a feed.
    print(f"Published to {topic} with PID {pid}")


def message(client, topic, message):
    print(f"New message on topic {topic}: {message}")

# Set up a MiniMQTT Client
mqtt_client = MQTT.MQTT(
    broker=mqtt_broker,
    port=1883,
    username=mqtt_username,
    password=mqtt_password,
    socket_pool=pool,
    is_ssl=False,
)

# Connect callback handlers to mqtt_client
mqtt_client.on_connect = connect
mqtt_client.on_disconnect = disconnect
mqtt_client.on_subscribe = subscribe
mqtt_client.on_unsubscribe = unsubscribe
mqtt_client.on_publish = publish
mqtt_client.on_message = message

try:
    print(f"Attempting to connect to {mqtt_client.broker}")
    mqtt_client.connect()

    while True:
        mqtt_client.loop()

        led.value = True

        touch = ss.moisture_read()
        temp = ss.get_temp()

        payload = json.dumps({
            "device_id": device_id,
            "name": plant_name,
            "temperature": temp,
            "moisture": touch,
            "firmware_version": firmware_version,
        })

        print(payload)
        mqtt_client.publish(mqtt_topic, payload)

        led.value = False
        time.sleep(5)
    
except KeyboardInterrupt:
    print("\n Execution interrupted by user (Ctrl+C).")

except ConnectionRefusedError:
    print(f" Error: Could not connect. Broker at {mqtt_broker} refused connection.")

except Exception as e:
    print(f" Unexpected error occurred: {e}")

finally:
    print("Cleaning up resources...")
    
    # Disconnect gracefully from the broker
    mqtt_client.disconnect()
