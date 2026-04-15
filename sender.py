import socket
import os
import time

HOST = "127.0.0.1"
PORT = 5001
VIDEO_FOLDER = "videos"
CHECK_INTERVAL = 5  # seconds
MAX_RETRIES = 3     # Number of times to retry a failed transfer

os.makedirs(VIDEO_FOLDER, exist_ok=True)

print("Sender started. Watching video folder...")

def send_file(filepath):
    filename = os.path.basename(filepath)
    
    # 1. Get file size and convert to Megabytes
    file_size_bytes = os.path.getsize(filepath)
    file_size_mb = file_size_bytes / (1024 * 1024)

    # 3. Automatic Retry Loop
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            print(f"Sending '{filename}' (Size: {file_size_mb:.2f} MB) - Attempt {attempt}/{MAX_RETRIES}...")
            
            # 2. Start the timer
            start_time = time.time()
            
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((HOST, PORT))

            # Send filename first
            client.sendall(filename.encode())
            response = client.recv(1024)

            if response != b"FILENAME_OK":
                print(f"Receiver did not accept filename for {filename}")
                client.close()
                continue # Skip to the next attempt

            # Send file data
            with open(filepath, "rb") as f:
                while True:
                    data = f.read(4096)
                    if not data:
                        break
                    client.sendall(data)

            client.sendall(b"EOF")

            # Wait for confirmation
            response = client.recv(1024)
            client.close()

            if response == b"OK":
                # 2. Stop the timer and calculate duration
                end_time = time.time()
                transfer_duration = end_time - start_time
                
                print(f"Transfer confirmed: {filename}")
                print(f"--> Time taken: {transfer_duration:.2f} seconds")
                
                os.remove(filepath)
                print(f"--> Deleted local file: {filename}\n")
                return True
            else:
                print(f"No valid confirmation for {filename}")

        except Exception as e:
            print(f"Error sending {filename}: {e}")
        
        # If the code reaches here, the transfer failed. Wait before retrying.
        if attempt < MAX_RETRIES:
            print("Transfer failed. Retrying in 2 seconds...\n")
            time.sleep(2)

    # If the loop finishes without returning True, all attempts failed
    print(f"CRITICAL ERROR: Failed to send {filename} after {MAX_RETRIES} attempts. Will try again later.\n")
    return False

# Main Loop
while True:
    files = [f for f in os.listdir(VIDEO_FOLDER) if f.endswith(".mp4")]
    files.sort()

    for file in files:
        filepath = os.path.join(VIDEO_FOLDER, file)
        send_file(filepath)

    time.sleep(CHECK_INTERVAL)