import socket
import time
import threading

open_ports = []
lock = threading.Lock()


def scan_port(host, port, timeout):
    try:
        sock = socket.socket()
        sock.settimeout(timeout)
        sock.connect((host, port))
        sock.close()
        service = get_service(port)
        with lock:
            print(f"[+] Port {port}/tcp is open ({service})")
        open_ports.append(port)
    except:
        pass 
    

def get_service(port):
    services = {
        21: "FTP",
        22: "SSH",
        23: "Telnet",
        25: "SMTP",
        53: "DNS",
        80: "HTTP",
        110: "POP3",
        143: "IMAP",
        443: "HTTPS",
        445: "SMB",
        3306: "MySQL",
        3389: "RDP",
        8080: "HTTP-Alt"
    }
    return services.get(port, "Unknown")

def measure_latency(host):
    try:
        sock = socket.socket()
        sock.settimeout(2)
        start = time.time()
        sock.connect((host, 80))
        latency = time.time() - start
        sock.close()
        return round(latency, 2)
    except:
        try:
            sock.close()
        except:
            pass
        return 1.0



print("=" * 50)
print(" RAJ`S PORT SCANNER v1.0")
print("=" * 50)

host = input("Enter the target host (IP or domain): ")
start_port = int(input("Enter the starting port number: "))
end_port = int(input("Enter the ending port number: "))

print(f"[*] Measuring latency to {host}...")
latency = measure_latency(host)
timeout = latency * 2
print(f"[*] Latency: {latency}s - Timeout set to: {timeout}s")
print(f"[*] Scanning ports {start_port} to {end_port} on {host}...")
print("-" * 50)

open_ports = []
start_time = time.time()
threads = []
for port in range(start_port, end_port + 1):
    t = threading.Thread(target=scan_port, args=(host, port, timeout))
    threads.append(t)
    t.start()
for t in threads:
    t.join()

end_time = time.time()
print("-" * 50)
print(f"Scan completed in {round(end_time - start_time, 2)} seconds.")
print(f"[*] {len(open_ports)} open ports found:")
print(f"[*] open ports: {sorted(open_ports)}")

