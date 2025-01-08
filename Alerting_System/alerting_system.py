from kafka import KafkaConsumer
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Kafka Configuration
LOG_TOPIC = "processed-logs"
BOOTSTRAP_SERVERS = "localhost:9092"

# Email Configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_ADDRESS = "sharvarighatake2000@gmail.com"  # Replace with your email
EMAIL_PASSWORD = "atrv tngb hlrh ufaz"  # Replace with your email password
ALERT_RECIPIENT = "jadhavdiksha5@gmail.com"  # Replace with recipient email

# Initialize Kafka Consumer
consumer = KafkaConsumer(
    LOG_TOPIC,
    bootstrap_servers=BOOTSTRAP_SERVERS,
    value_deserializer=lambda x: json.loads(x.decode("utf-8")),
    auto_offset_reset="earliest",
    group_id="alerting-group",
    enable_auto_commit=True,
)

def send_email_alert(log):
    """
    Send an email alert for critical logs.
    """
    try:
        subject = f"Critical Alert: {log.get('message', 'Unknown Issue')}"
        body = f"""
        Alert Details:
        Level: {log['severity']}
        Message: {log['message']}
        Timestamp: {log['processed_at']}
        """

        msg = MIMEMultipart()
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = ALERT_RECIPIENT
        msg["Subject"] = subject

        msg.attach(MIMEText(body, "plain"))

        # Connect to SMTP server and send email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, ALERT_RECIPIENT, msg.as_string())

        print(f"Alert sent: {subject}")

    except Exception as e:
        print(f"Failed to send alert: {e}")

print("Alerting System is running and listening for critical logs...")

try:
    for message in consumer:
        log = message.value
        print(f"Received processed log: {log}")

        # Check if the log level is critical
        if log.get("severity", "").upper() == "CRITICAL":
            print(f"Critical log detected: {log}")
            send_email_alert(log)

except KeyboardInterrupt:
    print("Shutting down Alerting System...")
finally:
    consumer.close()
