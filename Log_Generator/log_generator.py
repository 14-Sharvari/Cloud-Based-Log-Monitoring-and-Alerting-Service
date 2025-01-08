from kafka import KafkaProducer
import json
import time

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda x: json.dumps(x).encode('utf-8'),
)

# Example log levels and messages
log_levels = ["INFO", "WARN", "ERROR", "CRITICAL"]
log_messages = [
    "User logged in",
    "High memory usage",
    "Application crashed",
    "Server down"
]

while True:
    log = {
        "level": log_levels[int(time.time()) % len(log_levels)],
        "message": log_messages[int(time.time()) % len(log_messages)],
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    producer.send("logs", value=log)
    print(f"Sent log to Kafka: {log}")
    time.sleep(5)
