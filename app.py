from flask import Flask, jsonify, render_template
import psutil
import time
from threading import Thread

app = Flask(__name__, template_folder='.')

# --- 1. LOCAL DATA STORE FOR REAL METRICS ---
# Isme aapke laptop ka bilkul sachha raw hardware parameters save rahega
laptop_metrics = {
    "cpu_usage": 0,
    "ram_usage": 0,
    "total_ram": 0,
    "available_ram": 0,
    "active_tasks": 0,
    "cpu_status": "Normal",
    "ram_status": "Normal"
}

# --- 2. ASLI REAL-TIME HEALTH CORE ENGINE ---
def real_hardware_monitor_worker():
    print("⏰ Real Laptop Hardware Engine Active aur Live Monitoring Mode mein hai...")
    while True:
        try:
            # Direct Windows Kernel se live telemetry nikalna
            cpu = psutil.cpu_percent(interval=None)
            ram = psutil.virtual_memory()
            tasks_count = len(psutil.pids()) # Kitne background software chal rahe hain

            # Logical safety threshold limits trigger configurations
            cpu_state = "Online" if cpu <= 80 else "Offline"
            ram_state = "Online" if ram.percent <= 85 else "Offline"

            # Global array pipeline mein values transfer karna
            laptop_metrics["cpu_usage"] = cpu
            laptop_metrics["ram_usage"] = ram.percent
            laptop_metrics["total_ram"] = round(ram.total / (1024 ** 3), 2) # GB me convert karna
            laptop_metrics["available_ram"] = round(ram.available / (1024 ** 3), 2)
            laptop_metrics["active_tasks"] = tasks_count
            laptop_metrics["cpu_status"] = cpu_state
            laptop_metrics["ram_status"] = ram_state

        except Exception as e:
            print("Hardware link warnings:", e)
        time.sleep(2) # Har 2 second mein aapke laptop ka live status monitor hoga

# Separate processing engine thread generation
monitor_thread = Thread(target=real_hardware_monitor_worker, daemon=True)
monitor_thread.start()

# --- 3. PRODUCTION REST APIS & FRONTEND WEB VIEWS ---

@app.route('/')
def home():
    return render_template('dashboard.html')

@app.route('/api/v1/devices', methods=['GET'])
def get_real_telemetry():
    # Frontend grid mapping data package compilation array
    devices_structure = [
        {
            "device_id": 1,
            "device_name": f"Processor Core Engine (CPU) - Tasks: {laptop_metrics['active_tasks']}",
            "ip_address": f"Usage: {laptop_metrics['cpu_usage']}%",
            "status": laptop_metrics['cpu_status']
        },
        {
            "device_id": 2,
            "device_name": f"System RAM Cache (Total: {laptop_metrics['total_ram']} GB)",
            "ip_address": f"Free: {laptop_metrics['available_ram']} GB",
            "status": laptop_metrics['ram_status']
        }
    ]
    return jsonify(devices_structure)

if __name__ == '__main__':
    app.run(debug=True, port=5000, use_reloader=False)