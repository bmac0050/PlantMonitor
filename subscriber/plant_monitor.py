# Plant Monitor Subscriber
# by Brian McPhail
#
# This script subscribes to a MQTT topic and logs the data received from the plant monitor.


from os import getenv
from dotenv import load_dotenv
import paho.mqtt.client as mqtt
import json, logging
from datetime import datetime, UTC

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)

logger = logging.getLogger(__name__)

mqtt_host = getenv("MQTT_HOST")
mqtt_port = int(getenv("MQTT_PORT", "1883"))
mqtt_username = getenv("MQTT_USERNAME")
mqtt_password = getenv("MQTT_PASSWORD")
mqtt_topic = getenv("MQTT_TOPIC")

required_env_vars = {
    "MQTT_HOST": mqtt_host,
    "MQTT_PORT": mqtt_port,
    "MQTT_USERNAME": mqtt_username,
    "MQTT_PASSWORD": mqtt_password,
    "MQTT_TOPIC": mqtt_topic
}

for var in required_env_vars:
    if not getenv(var):
        raise ValueError(f"Environment variable '{var}' is not set")


def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        logger.info("Connected successfully")
    else:
        logger.error(f"Connection failed: {reason_code}")



def on_message(client, userdata, msg):
    payload = json.loads(msg.payload.decode())
    payload["timestamp"] = datetime.now(UTC).isoformat()
    logger.info("Device ID: %s", payload["device_id"])
    logger.info("Plant: %s", payload["name"])
    logger.info("Temperature: %s °C", payload["temperature"])
    logger.info("Moisture: %s", payload["moisture"])
    logger.info("Timestamp: %s", payload["timestamp"])


def on_subscribe(mqttc, obj, mid, reason_code_list, properties):
    logger.info("Subscribed: %s %s", mid, reason_code_list)


def on_log(mqttc, obj, level, string):
    logger.info(string)

def on_disconnect(client, userdata, disconnect_flags, reason_code, properties):
    if reason_code == 0:
        logger.info("Disconnected successfully.")
    else:
        logger.error(f"Unexpected disconnection: {reason_code}")


# If you want to use a specific client id, use
# mqttc = mqtt.Client("client-id")
# but note that the client id must be unique on the broker. Leaving the client
# id parameter empty will generate a random id for you.

def main():
    mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    mqttc.username_pw_set(
        username=mqtt_username,
        password=mqtt_password
    )
    mqttc.on_message = on_message
    mqttc.on_connect = on_connect
    mqttc.on_subscribe = on_subscribe
    mqttc.on_disconnect = on_disconnect
    # Uncomment to enable debug messages
    # mqttc.on_log = on_log
    mqttc.connect(mqtt_host, mqtt_port, 60)
    mqttc.subscribe(mqtt_topic, 0)

    try:
        mqttc.loop_forever()

    except KeyboardInterrupt:
        logger.info("Exiting...")

    finally:
        mqttc.disconnect()

if __name__ == "__main__":
    main()