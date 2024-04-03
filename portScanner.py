from tkinter import messagebox
import subprocess
import time

def get_open_ports():
    try:
        result = subprocess.run(["netstat", "-an"], capture_output=True, text=True)
        output_lines = result.stdout.splitlines()

        open_ports = set()

        for line in output_lines:
            if "LISTEN" in line:
                parts = line.split()
                if len(parts) >= 4:
                    address = parts[1]
                    if ":" in address:
                        port = address.split(":")[-1]
                    else:
                        port = address.split(".")[-1]
                    open_ports.add(port)

        return open_ports

    except Exception as e:
        print(f"An error occurred: {e}")
        return set()

def check_new_ports():
    current_ports = get_open_ports()
    if not hasattr(check_new_ports, 'previous_ports'):
        check_new_ports.previous_ports = current_ports
        return False

    new_ports = current_ports - check_new_ports.previous_ports
    if new_ports:
        messagebox.showwarning('Alert',"New ports opened")
        check_new_ports.previous_ports = current_ports
        return True
    else:
        print("No new ports opened.")
        check_new_ports.previous_ports = current_ports
        return False

if __name__ == "__main__":
    while True:
        check_new_ports()
        time.sleep(1)
