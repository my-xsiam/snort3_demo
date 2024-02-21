import paramiko
import time

def tail_remote_file(hostname, port, username, password, remote_file_path, interval=5):
    """Tail a remote file, printing new contents as they are written."""
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # Connect to the remote server
        client.connect(hostname, port=port, username=username, password=password)

        # Open SFTP session
        sftp = client.open_sftp()

        # Open the remote file
        remote_file = sftp.open(remote_file_path, "r")

        # Go to the end of the file
        remote_file.seek(0, 2)
        while True:
            # Read next line
            line = remote_file.readline()
            if not line:
                time.sleep(interval)  # Wait for a short period before trying again
                continue  # Retry reading in case of new data
            print(line.strip())
    except Exception as e:
        print(f"Failed to tail remote file: {e}")
    finally:
        try:
            remote_file.close()
            sftp.close()
        except:
            pass
        client.close()

# Configuration parameters
hostname = '192.168.20.236'
port = 22  # Default SSH port
username = 'root'
password = 'LAB_P@ssw0rd'
remote_file_path = '/var/lib/docker/volumes/juice_snortdata/_data/alert_json.txt'  # Path to the Snort alert file on the remote system
interval = 1  # Polling interval in seconds

# Start tailing the file
tail_remote_file(hostname, port, username, password, remote_file_path, interval)
