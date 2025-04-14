import socket
import threading
from queue import Queue

def port_scan(target, port):
    """Scan a single port on the target."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((target, port))
        if result == 0:
            print(f"Port {port} is open")
        sock.close()
    except Exception as e:
        pass

def threader(target, queue):
    """Thread worker to scan ports."""
    while True:
        port = queue.get()
        port_scan(target, port)
        queue.task_done()

def scan_ports(target, start_port, end_port):
    """Main function to scan a range of ports."""
    print(f"Scanning {target} from port {start_port} to {end_port}...")
    queue = Queue()
    
    # Start 100 threads
    for _ in range(100):
        t = threading.Thread(target=threader, args=(target, queue))
        t.daemon = True
        t.start()
    
    # Add ports to queue
    for port in range(start_port, end_port + 1):
        queue.put(port)
    
    queue.join()
    print("Scan complete.")

if __name__ == "__main__":
    target = input("Enter target IP or hostname: ")
    start_port = int(input("Enter start port: "))
    end_port = int(input("Enter end port: "))
    scan_ports(target, start_port, end_port)
import hashlib

def hash_password(password):
    """Hash a password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

def crack_password(target_hash, wordlist_file):
    """Attempt to crack a password using a wordlist."""
    try:
        with open(wordlist_file, 'r', encoding='utf-8') as file:
            for word in file:
                word = word.strip()
                hashed_word = hash_password(word)
                if hashed_word == target_hash:
                    print(f"Password found: {word}")
                    return True
                print(f"Trying: {word}")
        print("Password not found in wordlist.")
        return False
    except FileNotFoundError:
        print("Wordlist file not found.")
        return False

if __name__ == "__main__":
    target_password = input("Enter password to crack (will be hashed): ")
    target_hash = hash_password(target_password)
    wordlist = input("Enter path to wordlist file: ")
    crack_password(target_hash, wordlist)
import requests
import sys

def dir_brute(target_url, wordlist_file):
    """Brute-force directories on a web server."""
    try:
        with open(wordlist_file, 'r', encoding='utf-8') as file:
            for line in file:
                dir_name = line.strip()
                url = f"{target_url}/{dir_name}"
                try:
                    response = requests.get(url, timeout=2)
                    if response.status_code == 200:
                        print(f"Found directory: {url}")
                    elif response.status_code == 403:
                        print(f"Forbidden directory: {url}")
                except requests.RequestException:
                    pass
    except FileNotFoundError:
        print("Wordlist file not found.")
        sys.exit(1)

if __name__ == "__main__":
    target = input("Enter target URL (e.g., http://example.com): ")
    wordlist = input("Enter path to wordlist file: ")
    dir_brute(target, wordlist)