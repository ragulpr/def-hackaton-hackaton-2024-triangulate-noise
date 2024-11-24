import socket
import threading
import sys
from typing import List, Optional
import netifaces

class Connection:
    def __init__(self, socket: socket.socket, connection_id: int):
        self.socket = socket
        self.id = connection_id
        self.address = socket.getpeername()[0]
        self.port = socket.getpeername()[1]
        self.in_buffer = self.socket.makefile('r')
        self.out_buffer = self.socket.makefile('w')
        self.latest_event_time = None
        
    def send_message(self, message: str):
        try:
            self.out_buffer.write(f"{message}\n")
            self.out_buffer.flush()
        except Exception as e:
            print(f"Error sending message: {e}")
            
    def close_connection(self):
        try:
            self.socket.close()
            print(f"Connection {self.id} closed.")
        except Exception as e:
            print(f"Error closing connection: {e}")

class P2PNetwork:
    def __init__(self, port: int):
        self.connections: List[Connection] = []
        self.connection_id_counter = 1
        self.listening_port = port
        self.server_socket = None
        
    def start_server(self):
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind(('', self.listening_port))
            self.server_socket.listen(5)
            print(f"Server started on port {self.listening_port}")
            
            while True:
                client_socket, _ = self.server_socket.accept()
                connection = Connection(client_socket, self.connection_id_counter)
                self.connections.append(connection)
                self.connection_id_counter += 1
                threading.Thread(target=self.handle_connection, args=(connection,)).start()
                print(f"New connection from {connection.address}:{connection.port}")
                
        except Exception as e:
            print(f"Error starting server: {e}")
            
    def handle_connection(self, connection: Connection):
        try:
            while True:
                message = connection.in_buffer.readline().strip()
                if not message:
                    break
                
                # Handle noise detection messages
                if message.startswith("NOISE_DETECTED"):
                    try:
                        # Parse the message
                        parts = message.split()
                        amplitude = float(parts[1].split('=')[1])
                        timestamp = float(parts[2].split('=')[1])
                        connection.latest_event_time = timestamp
                        print(f"\nNoise detected by peer {connection.address}:{connection.port}")
                        print(f"Amplitude: {amplitude:.2f}, Time: {timestamp}")
                        print("> ", end='', flush=True)  # Restore command prompt
                    except Exception as e:
                        print(f"Error parsing noise detection message: {e}")
                else:
                    print(f"Message received from {connection.address}:{connection.port} - {message}")
                    
        except Exception as e:
            print(f"Connection error with {connection.address}:{connection.port}")
        finally:
            connection.close_connection()
            if connection in self.connections:
                self.connections.remove(connection)
                
    def connect(self, destination: str, port: int):
        try:
            # Only prevent connection to exact same pot 
                
            # Check for duplicate connections
            for conn in self.connections:
                if conn.address == destination and conn.port == port:
                    print(f"Error: Duplicate connection to {destination}:{port}")
                    return
                    
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((destination, port))
            connection = Connection(client_socket, self.connection_id_counter)
            self.connections.append(connection)
            self.connection_id_counter += 1
            threading.Thread(target=self.handle_connection, args=(connection,)).start()
            print(f"Connected to {destination}:{port}")
            
        except Exception as e:
            print(f"Error connecting to {destination}:{port}: {e}")
            
    def send(self, connection_id: int, message: str):
        connection = next((conn for conn in self.connections if conn.id == connection_id), None)
        if connection:
            connection.send_message(message)
            print(f"Message sent to Connection ID: {connection_id}")
        else:
            print(f"Error: Connection ID {connection_id} not found.")
            
    def list_connections(self):
        if not self.connections:
            print("No active connections.")
            return
            
        print("Active connections:")
        for conn in self.connections:
            print(f"Connection ID: {conn.id}, Address: {conn.address}, Port: {conn.port}")
            
    def terminate_connection(self, connection_id: int):
        connection = next((conn for conn in self.connections if conn.id == connection_id), None)
        if connection:
            try:
                if connection.socket.fileno() != -1:
                    connection.send_message("Connection is being terminated.")
            except Exception as e:
                print(f"Failed to send termination message: {e}")
            finally:
                connection.close_connection()
                self.connections.remove(connection)
                print(f"Connection {connection_id} terminated.")
        else:
            print(f"Error: Connection ID {connection_id} not found.")
            
    def terminate_all_connections(self):
        for connection in self.connections[:]:
            self.terminate_connection(connection.id)
            
    def get_my_ip(self):
        try:
            for interface in netifaces.interfaces():
                addrs = netifaces.ifaddresses(interface)
                if netifaces.AF_INET in addrs:
                    for addr in addrs[netifaces.AF_INET]:
                        ip = addr['addr']
                        if not ip.startswith('127.'):
                            return ip
            return "Could not determine external IP address."
        except Exception as e:
            return f"Error retrieving IP address: {e}"

def print_help():
    print("Available commands:")
    print("  help                           - Display this help message")
    print("  connect <destination> <port>   - Establish a new connection")
    print("  list                           - List all active connections")
    print("  send <connection id> <message> - Send a message to a specific connection")
    print("  terminate <connection id>      - Terminate a connection")
    print("  myip                           - Display your IP address")
    print("  myport                         - Display your port number")
    print("  exit                           - Exit the program")

def main():
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print("Invalid port")
            sys.exit(1)
    else:
        port = 4093
        
    network = P2PNetwork(port)
    server_thread = threading.Thread(target=network.start_server)
    server_thread.daemon = True
    server_thread.start()
    
    while True:
        try:
            command = input("> ").strip()
            parts = command.split(maxsplit=2)
            
            if not parts:
                continue
                
            cmd = parts[0].lower()
            
            if cmd == "help":
                print_help()
            elif cmd == "connect" and len(parts) == 3:
                network.connect(parts[1], int(parts[2]))
            elif cmd == "list":
                network.list_connections()
            elif cmd == "myip":
                print(f"My IP address: {network.get_my_ip()}")
            elif cmd == "myport":
                print(f"Listening on port: {network.listening_port}")
            elif cmd == "send" and len(parts) == 3:
                network.send(int(parts[1]), parts[2])
            elif cmd == "terminate" and len(parts) == 2:
                network.terminate_connection(int(parts[1]))
            elif cmd == "exit":
                print("Broadcasting a shutdown message to peers")
                network.terminate_all_connections()
                print("Shutting down peer...")
                break
            else:
                print("Unknown command. Type 'help' for available commands.")
                
        except KeyboardInterrupt:
            print("\nShutting down...")
            network.terminate_all_connections()
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
