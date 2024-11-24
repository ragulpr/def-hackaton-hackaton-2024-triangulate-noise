import pyaudio
import numpy as np
import sys
import time
import threading
from typing import Optional
from connection import P2PNetwork

class NoiseDetector:
    # Audio configuration constants
    CHUNK_SIZE = 1024  # Number of frames per buffer
    FORMAT = pyaudio.paFloat32  # Audio format (32-bit float)
    CHANNELS = 1  # Mono audio
    RATE = 44100  # Sampling rate (Hz)
    
    # Detection parameters
    THRESHOLD = 20  # Amplitude threshold for noise detection
    COOLDOWN = 1.0  # Seconds between detections to avoid multiple triggers

    def __init__(self, network=None):
        self.audio = None
        self.stream = None
        self.last_detection = 0
        self.network = network
        # Add buffer start time tracking
        self.buffer_start_time = 0
        self.latest_event = None
        
    def initialize_audio(self) -> None:
        """Initialize PyAudio and open microphone stream."""
        try:
            self.audio = pyaudio.PyAudio()
            
            # Find the first available input device
            input_device = None
            for i in range(self.audio.get_device_count()):
                device_info = self.audio.get_device_info_by_index(i)
                if int(device_info.get('maxInputChannels', 0)) > 0:
                    input_device = i
                    break
            
            if input_device is None:
                raise Exception("No input devices found")
                
            self.stream = self.audio.open(
                format=self.FORMAT,
                channels=self.CHANNELS,
                rate=self.RATE,
                input=True,
                input_device_index=input_device,
                frames_per_buffer=self.CHUNK_SIZE
            )
            print("Microphone initialized successfully!")
            print("Listening for loud noises... (Press Ctrl+C to exit)")
        except Exception as e:
            print(f"Error initializing audio: {str(e)}")
            raise

    def process_audio(self) -> Optional[tuple[float, float]]:
        """Process audio chunk and return (amplitude, exact_timestamp)."""
        try:
            # Record the exact time before reading the buffer
            buffer_start = time.time()
            data = np.frombuffer(
                self.stream.read(self.CHUNK_SIZE, exception_on_overflow=False),
                dtype=np.float32
            )
            
            # Calculate amplitude
            amplitude = np.max(np.abs(data))
            
            # Find the exact sample where the peak occurred
            peak_sample_index = np.argmax(np.abs(data))
            
            # Calculate the precise time of the peak
            # Each sample represents 1/RATE seconds
            seconds_per_sample = 1.0 / self.RATE
            peak_time_offset = peak_sample_index * seconds_per_sample
            exact_timestamp = buffer_start + peak_time_offset
            
            return amplitude, exact_timestamp, buffer_start
            
        except Exception as e:
            print(f"Error processing audio: {str(e)}")
            return None

    def detect_noise(self) -> None:
        """Main detection loop."""
        while True:
            try:
                result = self.process_audio()
                
                if result is None:
                    continue
                
                amplitude, exact_timestamp, buffer_start = result
                
                # Check if amplitude exceeds threshold and cooldown period has passed
                if (amplitude > self.THRESHOLD and 
                    exact_timestamp - self.last_detection > self.COOLDOWN):
                    self.last_detection = exact_timestamp
                    
                    latest_event_times = {
                        self.network.get_my_ip():exact_timestamp,
                        }

                    print(f"Locally detected noise. Amplitude={amplitude:.2f} Time={exact_timestamp:.6f} BufferStartTime={buffer_start} Now={time.time()}")
                    
                    # Send noise detection to all connected peers with precise timing
                    if self.network:
                        message = f"NOISE_DETECTED amplitude={amplitude:.2f} time={exact_timestamp:.6f}"
                        for conn in self.network.connections:
                            self.network.send(conn.id, message)
                            latest_event_times[conn.address]=conn.latest_event_time

                        # Validate event_dict 
                        timestamps = latest_event_times.values()
                        if None not in timestamps and max(timestamps)-min(timestamps)<self.CHUNK_SIZE:
                            self.latest_event = {
                                "event_times":latest_event_times,
                                "amplitude":amplitude
                            }
                            print(f"EVENT {self.latest_event}")

                            

            except KeyboardInterrupt:
                print("\nStopping noise detection...")
                break
            except Exception as e:
                print(f"Unexpected error: {str(e)}")
                break

    def cleanup(self) -> None:
        """Clean up audio resources."""
        if self.stream is not None:
            self.stream.stop_stream()
            self.stream.close()
        if self.audio is not None:
            self.audio.terminate()

    def run(self) -> None:
        """Run the noise detector."""
        self.initialize_audio()
        self.detect_noise()
        self.cleanup()

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <port>")
        sys.exit(1)

    port = int(sys.argv[1])
    network = P2PNetwork(port)
    
    # Start network server in a separate thread
    server_thread = threading.Thread(target=network.start_server)
    server_thread.daemon = True
    server_thread.start()

    # Create and run noise detector with network reference
    detector = NoiseDetector(network=network)
    
    # Start noise detection in a separate thread
    detector_thread = threading.Thread(target=detector.run)
    detector_thread.daemon = True
    detector_thread.start()

    print(f"My IP address: {network.get_my_ip()}")
    print(f"Listening on port: {network.listening_port}")

    # Main command loop
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
                print("CONNECTING")
                network.connect(parts[1], int(parts[2]))
            
        except KeyboardInterrupt:
            print("\nShutting down...")
            network.terminate_all_connections()
            detector.cleanup()
            break

if __name__ == "__main__":
    main()