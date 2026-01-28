"""
Green Computing Power Manager - Backend API (Real System Monitoring)
====================================================================
This module monitors ACTUAL system metrics and implements intelligent
power management algorithms based on real CPU, memory, and disk usage.

REQUIREMENTS: pip install flask flask-cors psutil
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import psutil
import time
import threading
from datetime import datetime
from collections import deque
import platform

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# CPU Power States Configuration
CPU_P_STATES = {
    'P0': {'power': 65, 'freq': '3.5 GHz', 'performance': 100},
    'P1': {'power': 45, 'freq': '2.5 GHz', 'performance': 70},
    'P2': {'power': 25, 'freq': '1.5 GHz', 'performance': 40},
    'P3': {'power': 10, 'freq': '0.8 GHz', 'performance': 20}
}

CPU_C_STATES = {
    'C0': {'power': 0, 'desc': 'Active'},
    'C1': {'power': 5, 'freq': 'Sleep', 'performance': 0},
    'C3': {'power': 1, 'freq': 'Deep Sleep', 'performance': 0}
}

class PowerManagementSystem:
    def __init__(self):
        self.components = {
            'cpu': {'state': 'P0', 'utilization': 0, 'power': 65, 'temp': 45},
            'ram': {'state': 'Active', 'power': 8, 'utilization': 0},
            'disk': {'state': 'Active', 'power': 7, 'lastAccess': 0},
            'display': {'state': 'On', 'power': 25, 'brightness': 100},
            'network': {'state': 'Active', 'power': 3, 'traffic': 0}
        }
        
        self.power_history = deque(maxlen=60)
        self.total_energy = 0.0
        self.energy_saved = 0.0
        self.start_time = time.time()
        self.auto_mode = True
        self.is_running = False
        self.logs = deque(maxlen=50)
        self.lock = threading.Lock()
        
        # Track disk activity
        self.last_disk_io = psutil.disk_io_counters()
        self.last_disk_activity_time = time.time()
        
        # Track network activity
        self.last_net_io = psutil.net_io_counters()
        
    def add_log(self, message, log_type='info'):
        timestamp = datetime.now().strftime('%H:%M:%S')
        with self.lock:
            self.logs.appendleft({
                'timestamp': timestamp,
                'message': message,
                'type': log_type
            })
    
    def get_total_power(self):
        with self.lock:
            return sum(comp['power'] for comp in self.components.values())
    
    def get_state(self):
        """Return state with camelCase keys to match frontend expectations"""
        with self.lock:
            current_power = sum(comp['power'] for comp in self.components.values())
            return {
                'components': self.components.copy(),
                'power_history': list(self.power_history),
                'total_energy': round(self.total_energy, 2),
                'energy_saved': round(self.energy_saved, 2),
                'logs': list(self.logs)[:10],
                'auto_mode': self.auto_mode,
                'is_running': self.is_running,
                'current_power': current_power
            }

power_system = PowerManagementSystem()

def get_real_system_metrics():
    """
    Gather ACTUAL system metrics using psutil
    This is the advantage of having a backend!
    """
    metrics = {}
    
    # CPU Utilization (percentage)
    metrics['cpu_percent'] = psutil.cpu_percent(interval=0.1)
    
    # CPU Frequency (if available)
    try:
        cpu_freq = psutil.cpu_freq()
        if cpu_freq:
            metrics['cpu_freq_current'] = cpu_freq.current
            metrics['cpu_freq_max'] = cpu_freq.max
    except:
        metrics['cpu_freq_current'] = None
        metrics['cpu_freq_max'] = None
    
    # CPU Temperature (if available - works on some systems)
    try:
        temps = psutil.sensors_temperatures()
        if temps:
            # Get the first available temperature sensor
            for name, entries in temps.items():
                if entries:
                    metrics['cpu_temp'] = entries[0].current
                    break
        else:
            metrics['cpu_temp'] = None
    except:
        metrics['cpu_temp'] = None
    
    # Memory (RAM) Usage
    mem = psutil.virtual_memory()
    metrics['ram_percent'] = mem.percent
    metrics['ram_used_gb'] = mem.used / (1024**3)
    metrics['ram_total_gb'] = mem.total / (1024**3)
    
    # Disk I/O Activity
    try:
        disk_io = psutil.disk_io_counters()
        metrics['disk_read_bytes'] = disk_io.read_bytes
        metrics['disk_write_bytes'] = disk_io.write_bytes
        metrics['disk_io'] = disk_io
    except:
        metrics['disk_io'] = None
    
    # Network I/O Activity
    try:
        net_io = psutil.net_io_counters()
        metrics['net_sent_bytes'] = net_io.bytes_sent
        metrics['net_recv_bytes'] = net_io.bytes_recv
        metrics['net_io'] = net_io
    except:
        metrics['net_io'] = None
    
    # Number of running processes
    metrics['process_count'] = len(psutil.pids())
    
    return metrics

def adaptive_power_management():
    """
    Core adaptive algorithm using REAL system metrics
    """
    # Get actual system data
    metrics = get_real_system_metrics()
    cpu_util = metrics['cpu_percent']
    
    # ==================================================================
    # CPU POWER STATE MANAGEMENT (Based on Real CPU Utilization)
    # ==================================================================
    if cpu_util < 10:
        new_cpu_state = 'C1'
        cpu_power = CPU_C_STATES['C1']['power']
        if power_system.components['cpu']['state'] != 'C1':
            power_system.add_log(f'CPU entering sleep (C1) - Real utilization: {cpu_util:.1f}%', 'success')
    elif cpu_util < 20:
        new_cpu_state = 'P3'
        cpu_power = CPU_P_STATES['P3']['power']
        if power_system.components['cpu']['state'] != 'P3':
            power_system.add_log(f'CPU in power saver (P3) - {cpu_util:.1f}%', 'success')
    elif cpu_util < 50:
        new_cpu_state = 'P2'
        cpu_power = CPU_P_STATES['P2']['power']
        if power_system.components['cpu']['state'] != 'P2':
            power_system.add_log(f'CPU switching to P2 - {cpu_util:.1f}%', 'info')
    elif cpu_util < 75:
        new_cpu_state = 'P1'
        cpu_power = CPU_P_STATES['P1']['power']
        if power_system.components['cpu']['state'] != 'P1':
            power_system.add_log(f'CPU switching to P1 - {cpu_util:.1f}%', 'info')
    else:
        new_cpu_state = 'P0'
        cpu_power = CPU_P_STATES['P0']['power']
        if power_system.components['cpu']['state'] != 'P0':
            power_system.add_log(f'CPU max performance (P0) - {cpu_util:.1f}%', 'warning')
    
    # Get real CPU temperature or simulate based on utilization
    if metrics['cpu_temp']:
        cpu_temp = metrics['cpu_temp']
    else:
        cpu_temp = 30 + (cpu_util * 0.3)  # Simulated if not available
    
    # Get frequency from power state
    if new_cpu_state in CPU_P_STATES:
        cpu_freq = CPU_P_STATES[new_cpu_state]['freq']
    else:
        cpu_freq = CPU_C_STATES[new_cpu_state]['freq']
    
    with power_system.lock:
        power_system.components['cpu'].update({
            'state': new_cpu_state,
            'frequency': cpu_freq,
            'utilization': round(cpu_util, 1),
            'power': cpu_power,
            'temp': round(cpu_temp, 1)
        })
    
    # ==================================================================
    # DISK POWER MANAGEMENT (Based on Real Disk I/O)
    # ==================================================================
    if metrics['disk_io']:
        current_disk_io = metrics['disk_io']
        
        # Check if there's been any disk activity
        if (current_disk_io.read_bytes != power_system.last_disk_io.read_bytes or
            current_disk_io.write_bytes != power_system.last_disk_io.write_bytes):
            # Disk activity detected
            power_system.last_disk_activity_time = time.time()
            if power_system.components['disk']['state'] == 'Standby':
                with power_system.lock:
                    power_system.components['disk']['state'] = 'Active'
                    power_system.components['disk']['power'] = 7
                power_system.add_log('Disk spinning up - Real I/O detected', 'info')
        
        power_system.last_disk_io = current_disk_io
    
    # Calculate idle time
    idle_time = time.time() - power_system.last_disk_activity_time
    current_time = time.time() - power_system.start_time
    
    if idle_time > 20 and power_system.components['disk']['state'] == 'Active':
        with power_system.lock:
            power_system.components['disk']['state'] = 'Standby'
            power_system.components['disk']['power'] = 2
        power_system.add_log(f'Disk standby - {idle_time:.0f}s idle', 'success')
    
    with power_system.lock:
        power_system.components['disk']['lastAccess'] = current_time - idle_time
    
    # ==================================================================
    # DISPLAY BRIGHTNESS (Based on Real CPU Activity)
    # ==================================================================
    if cpu_util < 15 and power_system.components['display']['brightness'] > 50:
        with power_system.lock:
            power_system.components['display']['brightness'] = 50
            power_system.components['display']['power'] = 12
        power_system.add_log('Display dimmed to 50% - Low system activity', 'success')
    elif cpu_util > 50 and power_system.components['display']['brightness'] < 100:
        with power_system.lock:
            power_system.components['display']['brightness'] = 100
            power_system.components['display']['power'] = 25
        power_system.add_log('Display brightness restored', 'info')
    
    # ==================================================================
    # NETWORK POWER MANAGEMENT (Based on Real Network I/O)
    # ==================================================================
    if metrics['net_io']:
        current_net_io = metrics['net_io']
        
        # Calculate network activity rate (bytes per second)
        net_bytes = (current_net_io.bytes_sent + current_net_io.bytes_recv) - \
                   (power_system.last_net_io.bytes_sent + power_system.last_net_io.bytes_recv)
        
        # If very low network activity, enter low power mode
        if net_bytes < 1000 and cpu_util < 20 and power_system.components['network']['state'] == 'Active':
            with power_system.lock:
                power_system.components['network']['state'] = 'Low Power'
                power_system.components['network']['power'] = 1
            power_system.add_log('Network low power mode - Minimal traffic', 'success')
        elif (net_bytes > 10000 or cpu_util > 40) and power_system.components['network']['state'] == 'Low Power':
            with power_system.lock:
                power_system.components['network']['state'] = 'Active'
                power_system.components['network']['power'] = 3
            power_system.add_log('Network active - Traffic detected', 'info')
        
        power_system.last_net_io = current_net_io
    
    # ==================================================================
    # RAM UTILIZATION (Real Memory Usage)
    # ==================================================================
    ram_util = metrics['ram_percent']
    with power_system.lock:
        power_system.components['ram']['utilization'] = round(ram_util, 1)

def update_energy_tracking():
    """Calculate and update energy consumption"""
    current_power = power_system.get_total_power()
    power_system.power_history.append(current_power)
    
    energy_increment = current_power / 3600
    power_system.total_energy += energy_increment
    
    max_power = 108
    energy_saved_increment = (max_power - current_power) / 3600
    power_system.energy_saved += max(0, energy_saved_increment)

def monitoring_loop():
    """Background monitoring thread"""
    print("📊 Monitoring thread started - Using REAL system metrics")
    while True:
        if power_system.is_running and power_system.auto_mode:
            try:
                adaptive_power_management()
                update_energy_tracking()
            except Exception as e:
                power_system.add_log(f'Error: {str(e)}', 'error')
                print(f"Error in monitoring: {e}")
        
        time.sleep(1)

# Start monitoring thread
monitor_thread = threading.Thread(target=monitoring_loop, daemon=True)
monitor_thread.start()

# API Endpoints
@app.route('/api/status', methods=['GET'])
def get_status():
    """Get current system status"""
    return jsonify(power_system.get_state())

@app.route('/api/control', methods=['POST'])
def control_system():
    """Control system"""
    data = request.json
    action = data.get('action')
    
    if action == 'start':
        power_system.is_running = True
        power_system.add_log('✓ System monitoring started - Using real metrics', 'info')
    elif action == 'stop':
        power_system.is_running = False
        power_system.add_log('⏸ System monitoring paused', 'info')
    elif action == 'toggle_auto':
        power_system.auto_mode = not power_system.auto_mode
        mode = 'enabled' if power_system.auto_mode else 'disabled'
        power_system.add_log(f'Adaptive management {mode}', 'info')
    elif action == 'reset':
        power_system.__init__()
        power_system.add_log('🔄 System reset', 'info')
    
    return jsonify({'success': True, 'state': power_system.get_state()})

@app.route('/api/report', methods=['GET'])
def generate_report():
    """Generate detailed energy report"""
    runtime = time.time() - power_system.start_time
    efficiency = 0
    if power_system.total_energy + power_system.energy_saved > 0:
        efficiency = (power_system.energy_saved / 
                     (power_system.total_energy + power_system.energy_saved)) * 100
    
    # Get current system info
    metrics = get_real_system_metrics()
    
    report = {
        'runtime_seconds': round(runtime, 1),
        'total_energy_wh': round(power_system.total_energy, 3),
        'energy_saved_wh': round(power_system.energy_saved, 3),
        'efficiency_percent': round(efficiency, 1),
        'average_power_w': round(power_system.total_energy / (runtime / 3600), 1) if runtime > 0 else 0,
        'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'system_info': {
            'platform': platform.system(),
            'cpu_count': psutil.cpu_count(),
            'ram_total_gb': round(metrics['ram_total_gb'], 2),
            'current_cpu_percent': round(metrics['cpu_percent'], 1)
        }
    }
    
    return jsonify(report)

@app.route('/api/system-info', methods=['GET'])
def get_system_info():
    """Get detailed system information"""
    metrics = get_real_system_metrics()
    return jsonify({
        'platform': platform.system(),
        'platform_version': platform.version(),
        'cpu_count': psutil.cpu_count(),
        'cpu_freq_current': metrics.get('cpu_freq_current'),
        'cpu_freq_max': metrics.get('cpu_freq_max'),
        'ram_total_gb': round(metrics['ram_total_gb'], 2),
        'ram_used_gb': round(metrics['ram_used_gb'], 2),
        'process_count': metrics['process_count']
    })

@app.route('/')
def index():
    return """
    <html>
    <head>
        <style>
            body { font-family: Arial; padding: 40px; background: #f0f8f0; }
            .success { color: #059669; font-size: 24px; font-weight: bold; }
            code { background: #e5e7eb; padding: 4px 8px; border-radius: 4px; }
            ul { line-height: 1.8; }
        </style>
    </head>
    <body>
        <h1>🌿 Green Computing Power Manager API</h1>
        <p class="success">✅ Backend running with REAL system monitoring!</p>
        <h3>Features:</h3>
        <ul>
            <li>✓ Real CPU utilization tracking</li>
            <li>✓ Real memory usage monitoring</li>
            <li>✓ Real disk I/O activity detection</li>
            <li>✓ Real network traffic monitoring</li>
            <li>✓ Adaptive power management algorithms</li>
        </ul>
        <h3>API Endpoints:</h3>
        <ul>
            <li><code>GET /api/status</code> - Get system status</li>
            <li><code>POST /api/control</code> - Control system</li>
            <li><code>GET /api/report</code> - Get energy report</li>
            <li><code>GET /api/system-info</code> - Get system information</li>
        </ul>
        <p style="background: #fef3c7; padding: 15px; border-left: 4px solid #f59e0b; margin-top: 20px;">
            <strong>Next Step:</strong> Open <code>index.html</code> in your browser
        </p>
    </body>
    </html>
    """

if __name__ == '__main__':
    print("=" * 70)
    print("🌿 Green Computing Power Manager - Backend Server")
    print("=" * 70)
    print("\n✓ Using REAL system metrics with psutil")
    print("\nAlgorithms implemented:")
    print("  1. ✓ CPU P-State Management (Real utilization)")
    print("  2. ✓ CPU C-State Management (Real idle detection)")
    print("  3. ✓ Adaptive Power Management (Real-time)")
    print("  4. ✓ Disk Spin-down (Real I/O monitoring)")
    print("  5. ✓ Display Adaptive Brightness (Real CPU activity)")
    print("  6. ✓ Network Power Management (Real traffic monitoring)")
    print("  7. ✓ Energy Tracking and Reporting")
    print("\n📊 System Information:")
    print(f"  Platform: {platform.system()} {platform.release()}")
    print(f"  CPU Cores: {psutil.cpu_count()}")
    print(f"  RAM: {psutil.virtual_memory().total / (1024**3):.1f} GB")
    print("\n🚀 Server starting on http://localhost:5000")
    print("📱 Open index.html in your browser")
    print("=" * 70 + "\n")
    
    app.run(debug=True, port=5000, host='0.0.0.0', threaded=True)