from http.server import BaseHTTPRequestHandler, HTTPServer
import subprocess
import time

start_time = time.time()

def run_command(command):
    """Runs a shell command and returns its output."""
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, check=True)
    return result.stdout.decode('utf-8')


def get_core_voltage():
    """Returns the core voltage."""
    try:
        output = run_command("vcgencmd measure_volts core")
        # Output is in the form "volt=1.20V" or similar
        voltage = output.split('=')[1].strip().replace('V', '')
        return float(voltage)
    except Exception as e:
        print(f"Error getting core voltage: {e}")
        return 0.0


def get_cpu_temp():
    """Returns the CPU temperature."""
    try:
        output = run_command("vcgencmd measure_temp")
        # Output is in the form "temp=50.0'C" or similar
        temp = output.split('=')[1].strip().replace("'C", '')
        return float(temp)
    except Exception as e:
        print(f"Error getting CPU temperature: {e}")
        return 0.0


def get_uptime():
    """Returns the uptime of the server in seconds."""
    current_time = time.time()
    uptime = current_time - start_time
    return uptime


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/metrics':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()

            # Metrics
            core_voltage = get_core_voltage()
            cpu_temp = get_cpu_temp()
            uptime = get_uptime()

            metrics = f"""
# HELP raspberry_pi_core_voltage Core Voltage of the Raspberry Pi.
# TYPE raspberry_pi_core_voltage gauge
raspberry_pi_core_voltage {core_voltage}

# HELP raspberry_pi_cpu_temperature CPU Temperature of the Raspberry Pi.
# TYPE raspberry_pi_cpu_temperature gauge
raspberry_pi_cpu_temperature {cpu_temp}
            
# HELP raspberry_pi_uptime_seconds The uptime of the Raspberry Pi server in seconds.
# TYPE raspberry_pi_uptime_seconds counter
raspberry_pi_uptime_seconds {uptime}
"""
            self.wfile.write(metrics.encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()


def run(server_class=HTTPServer, handler_class=RequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting httpd on port {port}...')
    httpd.serve_forever()


if __name__ == '__main__':
    run()
