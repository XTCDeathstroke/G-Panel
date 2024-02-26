# server_metrics.py

import time
import threading
from flask import Flask, jsonify, render_template
import psutil
import platform
import cpuinfo

app = Flask(__name__)

# Read configuration from config.txt in the same directory
def read_config(file_path):
    config = {}
    try:
        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()
                if line and not line.startswith('#'):  # Ignore comments and blank lines
                    key, value = line.split('=')
                    config[key.strip()] = value.strip()
    except FileNotFoundError:
        print(f"Error: Configuration file '{file_path}' not found.")
    except Exception as e:
        print(f"Error reading configuration file '{file_path}': {e}")
    return config

# Global variable to store configuration
config = read_config('config.txt')

def update_metrics():
    while True:
        try:
            # Update the metrics
            metrics = {}

            if config.get('SHOW_CPU_USAGE', '').lower() == 'true':
                metrics['CPU Usage'] = f"{psutil.cpu_percent()}%"
            if config.get('SHOW_GPU_USAGE', '').lower() == 'true':
                # Add code to get GPU usage (if available)
                metrics['GPU Usage'] = "N/A"  # Placeholder
            if config.get('SHOW_MEMORY_USAGE', '').lower() == 'true':
                memory_info = psutil.virtual_memory()
                metrics['Memory Usage'] = f"{memory_info.percent}%"
            if config.get('SHOW_DISK_USAGE', '').lower() == 'true':
                disk_usage = psutil.disk_usage('/')
                metrics['Disk Usage'] = f"{disk_usage.percent}%"

            # Add more metrics based on configuration settings

            # Store the metrics in a global variable (or database, etc.) accessible by the Flask routes
            app.metrics = metrics

            # Sleep for the specified update frequency
            time.sleep(int(config.get('UPDATE_FREQUENCY', 60)))  # Default update frequency is 60 seconds
        except Exception as e:
            print(f"Error updating metrics: {e}")

# Start the thread to update metrics
update_thread = threading.Thread(target=update_metrics)
update_thread.daemon = True  # Daemonize the thread so it will be terminated when the main thread exits
update_thread.start()

@app.route('/')
def homepage():
    # Fetch system specifications
    system_info = {
        'Operating System': platform.platform(),
        'Processor': cpuinfo.get_cpu_info()['brand_raw'],
        # Add more system specifications as needed
    }
    return render_template('index.html', config=config, metrics=app.metrics, system_info=system_info)

@app.route('/metrics')
def metrics():
    # Return the metrics stored in the global variable
    return jsonify(app.metrics)

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True, host=config.get('IP_ADDRESS', '127.0.0.1'))


