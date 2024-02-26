# server_metrics.py

from flask import Flask, jsonify
import psutil

app = Flask(__name__)

def read_config(file_path):
    config = {}
    with open(file_path, 'r') as file:
        for line in file:
            if '=' in line:
                key, value = line.strip().split('=')
                config[key.strip()] = value.strip()
    return config

config = read_config('config.txt')  # Read configuration from config.txt

# Determine host address based on configuration
if config.get('LOCAL', '').lower() == 'true':
    host_address = '127.0.0.1'
else:
    host_address = config.get('IP_ADDRESS', '127.0.0.1')  # Default to localhost if IP address is not provided

@app.route('/metrics')
def metrics():
    cpu_percent = psutil.cpu_percent()
    mem_percent = psutil.virtual_memory().percent
    disk_percent = psutil.disk_usage('/').percent
    network_activity = "High"  # Placeholder for network activity (replace with actual implementation)
    alerts = ["Disk Space Low"]  # Placeholder for alerts (replace with actual implementation)

    return jsonify({
        "CPU Usage": f"{cpu_percent}%",
        "Memory Utilization": f"{mem_percent}%",
        "Disk Usage": f"{disk_percent}%",
        "Network Activity": network_activity,
        "Alerts": alerts
    })

if __name__ == '__main__':
    app.run(debug=True, host=host_address)  # Use host_address determined from config.txt
