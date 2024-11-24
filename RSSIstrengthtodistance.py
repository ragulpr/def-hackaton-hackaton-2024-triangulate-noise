import os
import re

def calculate_distance(rssi, tx_power=-59, path_loss_exponent=2):
    """
    Calculate the distance from RSSI using the path loss model.
    Args:
        rssi (int): Received Signal Strength Indicator (RSSI) in dBm.
        tx_power (int): RSSI value at 1 meter (default -59 dBm).
        path_loss_exponent (float): Path loss exponent (default 2 for free space).
    Returns:
        float: Estimated distance in meters.
    """
    # Formula: d = 10 ^ ((TX_POWER - RSSI) / (10 * n))
    distance = 10 ** ((tx_power - rssi) / (10 * path_loss_exponent))
    return round(distance, 2)

def get_wifi_signal_strength(interface, tx_power=-59, path_loss_exponent=2):
    """
    Fetch the Wi-Fi signal strength (RSSI) for a given interface and calculate distance.
    Args:
        interface (str): The Wi-Fi interface name (e.g., wlan0).
        tx_power (int): RSSI value at 1 meter (default -59 dBm).
        path_loss_exponent (float): Path loss exponent (default 2 for free space).
    Returns:
        list: A list of dictionaries with SSID, RSSI, and distance in meters.
    """
    try:
        # Use the iw command to scan for Wi-Fi networks
        result = os.popen(f"iw dev {interface} scan").read()
        
        # Parse the results to extract SSID and signal strength
        networks = []
        ssid = None
        for line in result.splitlines():
            if "SSID:" in line:
                ssid = line.split("SSID:")[1].strip()
            if "signal:" in line:
                rssi_match = re.search(r"signal:\s(-?\d+) dBm", line)
                if rssi_match and ssid:
                    rssi = int(rssi_match.group(1))
                    distance = calculate_distance(rssi, tx_power, path_loss_exponent)
                    networks.append({"SSID": ssid, "RSSI": rssi, "Distance (m)": distance})
                    ssid = None  # Reset for the next network
        
        return networks

    except Exception as e:
        print(f"Error: {e}")
        return []

# Example usage
if __name__ == "__main__":
    wifi_interface = "wlan0"  # Replace with your Wi-Fi interface name
    tx_power = -59  # RSSI at 1 meter
    path_loss_exponent = 2  # Environment factor

    networks = get_wifi_signal_strength(wifi_interface, tx_power, path_loss_exponent)
    if networks:
        print("Detected Networks:")
        for network in networks:
            print(f"SSID: {network['SSID']}, Signal Strength: {network['RSSI']} dBm, Distance: {network['Distance (m)']} meters")
    else:
        print("No networks detected.")
