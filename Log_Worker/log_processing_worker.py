from kafka import KafkaConsumer, KafkaProducer
import json
import time
from google.cloud import storage

# Kafka Configuration
LOG_TOPIC = "logs"  # Topic to consume raw logs
PROCESSED_TOPIC = "processed-logs"  # Topic to produce processed logs
BOOTSTRAP_SERVERS = 'localhost:9092'  # Kafka server address
GCS_BUCKET_NAME = 'log-monitor-bucket'

# Initialize Kafka Consumer
consumer = KafkaConsumer(
    LOG_TOPIC,
    bootstrap_servers=BOOTSTRAP_SERVERS,
    value_deserializer=lambda x: x.decode('utf-8'),  # Decode as a string first
    auto_offset_reset='earliest',
    group_id='log-processing-group',
    enable_auto_commit=True,
)

# Initialize Kafka Producer
producer = KafkaProducer(
    bootstrap_servers=BOOTSTRAP_SERVERS,
    value_serializer=lambda x: json.dumps(x).encode('utf-8'),
)

def validate_log(log):
    """
    Validate log message. Returns True if valid, False otherwise.
    """
    try:
        log_data = json.loads(log)  # Try parsing the JSON
        required_fields = {'level', 'message'}
        if not all(field in log_data for field in required_fields):
            return False  # Missing required fields
        return True
    except json.JSONDecodeError:
        return False  # Invalid JSON
    
def upload_to_gcs(bucket_name, file_name, content):
    """Upload a file's content to a GCS bucket."""
    # Initialize GCS client
    client = storage.Client()
    
    # Get the bucket
    bucket = client.get_bucket(bucket_name)
    
    # Create a new blob (object) in the bucket
    blob = bucket.blob(file_name)
    
    # Upload content
    blob.upload_from_string(content)

    print(f"Uploaded {file_name} to bucket {bucket_name}")

def process_log(raw_log):
    """
    Process a raw log entry and upload it to GCS.
    
    Args:
        raw_log (dict): A dictionary containing raw log data.
    
    Returns:
        dict: Processed log data with additional fields.
    """
    # Define severity mapping
    severity_mapping = {
        "INFO": "low",
        "WARN": "medium",
        "ERROR": "high",
        "CRITICAL": "critical"
    }
    
    # Example log processing logic
    processed_log = {
        "timestamp": raw_log.get("timestamp"),
        "message": raw_log.get("message"),
        "severity": severity_mapping.get(raw_log.get("level"), "unknown")  # Use the severity mapping
    }
    
    # Add additional metadata to the log
    processed_log["processed_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
    
    # Serialize the processed log to JSON
    processed_log_json = json.dumps(processed_log)
    
    # Generate a unique filename for the log file in GCS
    log_filename = f"processed_log_{int(time.time())}.json"
    
    # Upload the processed log to GCS
    upload_to_gcs(GCS_BUCKET_NAME, log_filename, processed_log_json)
    print(f"Processed log uploaded to GCS as {log_filename}")
    
    return processed_log

try:
    for message in consumer:
        raw_log = message.value
        print(f"Received raw log from Kafka: {raw_log}")

        # Validate the log before processing
        if not validate_log(raw_log):
            print(f"Invalid log skipped: {raw_log}")
            continue

        # Parse and process the log
        log_data = json.loads(raw_log)
        processed_log = process_log(log_data)
        print(f"Processed log: {processed_log}")

        # Send the processed log to the "processed-logs" Kafka topic
        producer.send(PROCESSED_TOPIC, value=processed_log)
        print(f"Processed log sent to Kafka topic '{PROCESSED_TOPIC}'")

except KeyboardInterrupt:
    print("Shutting down Log Processing Worker...")
finally:
    consumer.close()
    producer.close()
