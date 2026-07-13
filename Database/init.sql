CREATE TABLE IF NOT EXISTS raw.plant_readings (
    id SERIAL PRIMARY KEY,
    device_id VARCHAR(50),
    plant_name VARCHAR(50),
    temperature_c FLOAT,
    moisture FLOAT,
    weather_timestamp TIMESTAMPTZ,
    retrieved_at TIMESTAMPTZ
);