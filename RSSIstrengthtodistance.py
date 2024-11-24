import socket
import threading
import os
import re
import time

# Constants for RSSI to distance calculation
TX_POWER = -59  # RSSI at 1 meter
PATH_LOSS_EXPONENT = 2  # Environment factor (free space)

# Port for communication
PORT = 12345

def calculate_distance(rssi, tx_power=TX_POWER, path_loss_exponent=PATH_LOSS_EXPONENT):
    """
    Calculate the distance from RSSI using the path loss model.
    Args:
        rssi (int): Received Signal Strength Indicator (RSSI) in dBm.
        tx_power (int): RSSI value at 1 meter (default -59 dBm).
        path_loss_exponent (float): Path loss exponent (default 2 for free space).
    Returns:
        float: Estimated distance in meters.
    """
    distance = 10 ** ((tx_power - rssi) / (10 * path_loss_exponent))
    return round(distance, 2)

def get_device_rssi(interface="wlan0"):
    """
    Get the RSSI value for the current Wi-Fi network.
    Args:
        interface (str): The Wi-Fi interface name (e.g., wlan0).
    Returns:
        int: RSSI value in dBm or None if not found.
    """
    try:
        result = os.popen(f"iw dev {interface} link").read()
        rssi_match = re.search(r"signal:\s(-?\d+) dBm", result)
        if rssi_match:
            return int(rssi_match.group(1))
        else:
            return None
    except Exception as e:
        print(f"Error retrieving RSSI: {e}")
        return None

def server_thread(peer_ip, peer_port):
    """
    Server function to listen for incoming messages.
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(("0.0.0.0", PORT))
    print(f"Listening on port {PORT}...")

    while True:
        try:
            data, addr = server_socket.recvfrom(1024)
            message = data.decode()
            print(f"Received from {addr}: {message}")
            
            # Parse RSSI from the received message
            if "RSSI" in message:
                peer_rssi = int(message.split(":")[1].strip())
                local_rssi = get_device_rssi()
                if local_rssi:
                    distance = calculate_distance(peer_rssi)
                    print(f"Distance to {addr[0]}: {distance} meters")
        except Exception as e:
            print(f"Server error: {e}")

def client_thread(peer_ip, peer_port):
    """
    Client function to send RSSI data to the peer.
    """
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        try:
            local_rssi = get_device_rssi()
            if local_rssi is not None:
                message = f"RSSI:{local_rssi}"
                client_socket.sendto(message.encode(), (peer_ip, peer_port))
                print(f"Sent to {peer_ip}:{peer_port}: {message}")
            else:
                print("Failed to retrieve RSSI")
            time.sleep(2)  # Send data every 2 seconds
        except Exception as e:
            print(f"Client error: {e}")

if __name__ == "__main__":
    peer_ip = input("Enter peer device IP address: ")
    peer_port = PORT

    # Start server and client threads
    threading.Thread(target=server_thread, args=(peer_ip, peer_port), daemon=True).start()
    threading.Thread(target=client_thread, args=(peer_ip, peer_port), daemon=True).start()

    # Keep the main thread alive
    while True:
        time.sleep(1)
