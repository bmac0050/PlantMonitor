# Plant Monitor

An IoT plant monitoring system built with Raspberry Pi Pico W, MQTT, Python, Docker, and PostgreSQL.

The goal of this project is to monitor the moisture and temperature of household plants, collect historical sensor data, and eventually provide dashboards and notifications when plants need watering.

---

## Project Status

**Current Phase:** MQTT Subscriber Containerized

### Completed

- Raspberry Pi Pico W sensor node
- Adafruit STEMMA Soil Sensor (Seesaw)
- Wi-Fi connectivity
- MQTT publishing
- Mosquitto MQTT broker running in Docker on Raspberry Pi 4
- Python MQTT subscriber
- Dockerized subscriber
- Environment variable configuration using `.env`

### Planned

- Store readings in PostgreSQL
- Historical data and trends
- Dashboard
- Low-moisture notifications
- Support for multiple plant sensors

---

## System Architecture

```text
           Raspberry Pi Pico W
                   │
                   │
         Temperature / Moisture
                   │
                   ▼
            MQTT Publish
                   │
                   ▼
        Mosquitto MQTT Broker
        (Raspberry Pi 4 Docker)
                   │
                   ▼
      Plant Monitor Subscriber
           (Python + Docker)
                   │
                   ▼
          PostgreSQL Database
                   │
                   ▼
      Dashboard / Notifications
```

---

## Technologies Used

- Python 3.11
- Docker
- MQTT
- Eclipse Mosquitto
- Raspberry Pi Pico W
- Raspberry Pi 4
- CircuitPython
- Adafruit Seesaw Library
- PostgreSQL (planned)

---

## Repository Structure

```text
PlantMonitor/
│
├── pico/
│   └── code.py
│
├── subscriber/
│   ├── plant_monitor.py
│   ├── Dockerfile
│   ├── requirements.txt
│   └── .dockerignore
│
├── docker/
│
├── docs/
│
└── README.md
```

---

## MQTT Message Format

Example payload published by the Pico W:

```json
{
    "device_id": "pico01",
    "name": "Leafy",
    "firmware_version": "0.1",
    "temperature": 25.8,
    "moisture": 378,
    "timestamp": "2026-06-26T22:15:41Z"
}
```

---

## Docker

Build the subscriber image:

```bash
docker build -t plant-monitor-subscriber:0.1 .
```

Run the container:

```bash
docker run --rm \
  --env-file .env \
  plant-monitor-subscriber:0.1
```

---

## Database (Planned)

Database:

```
plantdb
```

Schema:

```
raw
```

Table:

```
plant_readings
```

Planned columns:

| Column | Description |
|---------|-------------|
| id | Primary key |
| device_id | Sensor device identifier |
| plant_name | Plant name |
| temperature_c | Temperature in Celsius |
| moisture | Raw moisture reading |
| reading_timestamp | Time measurement was taken |
| received_timestamp | Time subscriber received message |

---

## Future Enhancements

- Multiple plant support
- Automatic reconnect handling
- PostgreSQL persistence
- Dashboard with historical graphs
- Moisture threshold alerts
- OTA firmware updates
- Cloud synchronization
- Home Assistant integration

---

## Lessons Learned

This project demonstrates:

- Building an end-to-end IoT pipeline
- MQTT publish/subscribe architecture
- Docker containerization
- Environment variable management
- Python application structure
- Raspberry Pi networking
- Embedded development with CircuitPython

---

## Author

Brian McPhail

Personal learning project focused on IoT, automation, Docker, and cloud technologies.