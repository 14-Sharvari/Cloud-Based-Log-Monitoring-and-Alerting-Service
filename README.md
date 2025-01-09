# Cloud-Based-Log-Monitoring-and-Alerting-Service

## Authors
- *Diksha Jadhav*
- *Sharvari Ghatake*

---

## Project Overview
The *Real-Time Log Processing and Alerting System* is designed to handle high-volume log data streams in real-time. By leveraging Apache Kafka, Python, and a Flask API, the system processes logs, detects critical events, and sends immediate email alerts to stakeholders. It also provides a Flask-based REST API for querying processed log data.

This scalable and efficient system is well-suited for applications requiring real-time log monitoring, such as server performance tracking, error detection, and application diagnostics.

---

## Features
- *High Throughput*: Processes thousands of logs per second with minimal latency.
- *Critical Event Detection*: Identifies critical logs using predefined rules.
- *Real-Time Alerts*: Sends email notifications for critical events.
- *REST API*: Provides an interface to query processed logs and system metrics.
- *Scalable Design*: Uses modular components to handle varying workloads.

---

## System Architecture
The system consists of the following components:
1. *Apache Kafka*: Buffers and streams logs to downstream consumers.
2. *Python Processor*: Analyzes logs to detect critical events.
3. *SMTP*: Sends email notifications for flagged critical logs.
4. *Flask API*: Provides a RESTful interface to access processed log data and system status.

The components interact seamlessly to ensure real-time processing, alerting, and data access.

---

## Prerequisites
### Software Requirements
- *Python 3.8+*
- *Apache Kafka*
- *pip* (Python package manager)

### Python Libraries
The required Python libraries are listed in requirements.txt and include:
- kafka-python
- smtplib
- email
- flask
- flask-restful

---

# Setup and Installation

## Step 1: Clone the Repository
bash

git clone https://github.com/cu-csci-4253-datacenter-fall-2024/finalproject-final-project-team-94.git

cd finalproject-final-project-team-94

## Step 2: Install Dependencies
Install the required Python libraries:

bash

pip install -r requirements.txt

## Step 3: Set Up Apache Kafka
1. Download and install Apache Kafka.
2. Start Zookeeper:
   
   bash
   
   bin/zookeeper-server-start.sh config/zookeeper.properties
   
4. Start Kafka broker:
   
   bash
   
   bin/kafka-server-start.sh config/server.properties
   
6. Create a Kafka topic for logs:
   
   bash
   
   bin/kafka-topics.sh --create --topic logs --bootstrap-server localhost:9092
   
## Step 4: Configure SMTP
Update config.py with your SMTP server credentials:

python

SMTP_SERVER = "smtp.example.com"

SMTP_PORT = 587

SMTP_USERNAME = "your-email@example.com"

SMTP_PASSWORD = "your-password"

RECEIVER_EMAIL = "receiver-email@example.com"

## Step 5: Run the Python Log Processor
bash

python log_processor.py

## Step 6: Simulate Logs
Run the log generator to simulate real-time logs:

bash

python log_generator.py

## Step 7: Run the Flask API
Start the Flask application:

bash

python app.py

By default, the Flask app will run on [http://127.0.0.1:5000](http://127.0.0.1:5000).

# Accessing the Flask API
The Flask API provides endpoints to query processed logs and system status. Below are the key endpoints:

### Fetch Processed Logs
*GET* /logs

*Example Request:*

bash

curl http://127.0.0.1:5000/logs

### Fetch Summary of Logs
*GET* /logs

*Example Request:*

bash

curl http://127.0.0.1:5000/summary


# Testing

- *Simulated Logs:* Use the log generator to send test data.
- *Critical Event Rules:* Customize log detection rules in log_processor.py and validate alerts.
- *API Testing:* Use tools like Postman or curl to interact with the Flask API and ensure correct responses.
- *Performance Testing:* Evaluate throughput and latency under different workloads.

# Troubleshooting

- *No Alerts Received:* Verify SMTP credentials and network access.
- *API Not Accessible:* Ensure Flask is running and not blocked by firewalls.
- *Consumer Lag:* Check Kafka monitoring tools for potential backlogs.
- *High Latency:* Increase Kafka broker resources or optimize the Python processor.

# Future Scope

- Extend the REST API to include advanced log filtering and querying.
- Integrate SMS and push notifications for critical alerts.
- Use machine learning models for anomaly detection in logs.
