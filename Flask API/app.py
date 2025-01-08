from flask import Flask, request, jsonify, render_template_string
import csv
import os
from datetime import datetime

app = Flask(__name__)

LOG_FILE = 'logs.csv'

HOME_PAGE_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Real-Time Log Monitoring API</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f9;
            color: #333;
            margin: 0;
            padding: 0;
        }
        header {
            background-color: #0073e6;
            color: white;
            padding: 20px 0;
            text-align: center;
        }
        h1 {
            margin: 0;
            font-size: 2.5em;
        }
        p {
            margin: 10px 0;
        }
        .container {
            padding: 20px;
            max-width: 800px;
            margin: 20px auto;
            background: white;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            border-radius: 8px;
        }
        ul {
            list-style-type: none;
            padding: 0;
        }
        li {
            background: #0073e6;
            color: white;
            padding: 10px;
            margin: 5px 0;
            border-radius: 4px;
            text-align: center;
        }
        li a {
            color: white;
            text-decoration: none;
        }
        li a:hover {
            text-decoration: underline;
        }
        footer {
            text-align: center;
            padding: 10px;
            background-color: #f4f4f9;
            color: #666;
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <header>
        <h1>Real-Time Log Monitoring API</h1>
        <p>Monitor, Ingest, and Fetch Logs Effortlessly</p>
    </header>
    <div class="container">
        <h2>Available Endpoints</h2>
        <ul>
            <li><a href="/ping">Ping API</a> - Check API status</li>
            <li><a href="/logs">Fetch Logs</a> - View all logs</li>
            <li><a href="/summary">Log Summary</a> - View log statistics</li>
            <li><a href="#" onclick="alert('Use a POST tool like Postman to test this endpoint')">Ingest Log</a> - Add a new log</li>
        </ul>
        <p><b>Note:</b> Use Postman or other tools for POST endpoints like `/ingest-log`.</p>
    </div>
    <footer>
        <p>&copy; {{ year }} Real-Time Log Monitoring API</p>
    </footer>
</body>
</html>
"""

TABLE_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Logs</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f4f4f9;
            color: #333;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 20px;
        }
        th, td {
            border: 1px solid #ddd;
            text-align: left;
            padding: 8px;
        }
        th {
            background-color: #0073e6;
            color: white;
        }
        tr:nth-child(even) {
            background-color: #f2f2f2;
        }
    </style>
</head>
<body>
    <h1>Log Records</h1>
    <table>
        <thead>
            <tr>
                <th>Timestamp</th>
                <th>Level</th>
                <th>Message</th>
            </tr>
        </thead>
        <tbody>
            {% for log in logs %}
            <tr>
                <td>{{ log.timestamp }}</td>
                <td>{{ log.level }}</td>
                <td>{{ log.message }}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</body>
</html>
"""

SUMMARY_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Log Summary</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f4f4f9;
            color: #333;
        }
        table {
            width: 50%;
            border-collapse: collapse;
            margin: 20px auto;
            background: white;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            border-radius: 8px;
        }
        th, td {
            border: 1px solid #ddd;
            text-align: center;
            padding: 8px;
        }
        th {
            background-color: #0073e6;
            color: white;
        }
        tr:nth-child(even) {
            background-color: #f2f2f2;
        }
        h1 {
            text-align: center;
        }
        p {
            text-align: center;
        }
    </style>
</head>
<body>
    <h1>Log Summary</h1>
    <table>
        <thead>
            <tr>
                <th>Log Level</th>
                <th>Count</th>
            </tr>
        </thead>
        <tbody>
            {% for level, count in summary.items() %}
            <tr>
                <td>{{ level }}</td>
                <td>{{ count }}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
    <p>Total Logs: {{ total_logs }}</p>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HOME_PAGE_HTML, year=datetime.now().year)

@app.route('/ping', methods=['GET'])
def ping():
    html_response = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>API Health Check</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f4f4f9;
                color: #333;
                text-align: center;
                padding: 20px;
            }
            .container {
                background-color: white;
                padding: 20px;
                margin: 20px auto;
                max-width: 400px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
                border-radius: 8px;
            }
            h1 {
                color: #0073e6;
            }
            p {
                font-size: 1.2em;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>API Health Check</h1>
            <p><strong>Status:</strong> OK</p>
            <p><strong>Timestamp:</strong> {{ timestamp }}</p>
        </div>
    </body>
    </html>
    """
    return render_template_string(html_response, timestamp=datetime.now().isoformat())

@app.route('/logs', methods=['GET'])
def fetch_logs():
    try:
        if not os.path.exists(LOG_FILE):
            return render_template_string("<h1>No logs found</h1>")

        with open(LOG_FILE, 'r') as file:
            logs = list(csv.DictReader(file))
        
        # Apply filters
        level = request.args.get('level')
        start_time = request.args.get('start_time')
        end_time = request.args.get('end_time')
        
        if level:
            logs = [log for log in logs if log['level'].lower() == level.lower()]
        
        if start_time:
            try:
                start_time = datetime.fromisoformat(start_time)
                logs = [
                    log for log in logs 
                    if log.get('timestamp') and datetime.fromisoformat(log['timestamp']) >= start_time
                ]
            except ValueError:
                return jsonify({"status": "Error", "message": "Invalid start_time format. Use ISO 8601 format."}), 400
        
        if end_time:
            try:
                end_time = datetime.fromisoformat(end_time)
                logs = [
                    log for log in logs 
                    if log.get('timestamp') and datetime.fromisoformat(log['timestamp']) <= end_time
                ]
            except ValueError:
                return jsonify({"status": "Error", "message": "Invalid end_time format. Use ISO 8601 format."}), 400
        
        logs = [{"timestamp": log.get("timestamp", ""),
                 "level": log.get("level", ""),
                 "message": log.get("message", "")} for log in logs]

        return render_template_string(TABLE_TEMPLATE, logs=logs)

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"status": "Error", "message": str(e)}), 500


@app.route('/ingest-log', methods=['POST'])
def ingest_log():
    try:
        # Get the log data from the request
        log = request.get_json()
        if not log or 'level' not in log or 'message' not in log:
            return jsonify({"status": "Invalid data. 'level' and 'message' fields are required"}), 400

        # Add a timestamp if it's missing
        if 'timestamp' not in log:
            log['timestamp'] = datetime.now().isoformat()

        # Ensure the log file exists and append the log
        file_exists = os.path.exists(LOG_FILE)
        with open(LOG_FILE, 'a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['level', 'message', 'timestamp'])
            if not file_exists:  # Write the header if the file doesn't exist
                writer.writeheader()
            writer.writerow(log)

        print(f"Log received and written: {log}")
        return jsonify({"status": "Log received", "log": log}), 200

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"status": "Error", "message": str(e)}), 500

@app.route('/summary', methods=['GET'])
def log_summary():
    try:
        if not os.path.exists(LOG_FILE):
            return render_template_string("<h1>No logs found</h1>")

        # Count log levels
        with open(LOG_FILE, 'r') as file:
            logs = list(csv.DictReader(file))
        summary = {}
        for log in logs:
            level = log['level'].upper()
            summary[level] = summary.get(level, 0) + 1

        total_logs = len(logs)

        # Render HTML table
        return render_template_string(SUMMARY_TEMPLATE, summary=summary, total_logs=total_logs)

    except Exception as e:
        print(f"Error: {e}")
        return render_template_string(f"<h1>Error: {e}</h1>")


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
