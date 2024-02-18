import socket

def check_internet_connection(host="8.8.8.8", port=53, timeout=3):
    """
    Check if the Raspberry Pi is connected to the internet.
    
    Attempts to establish a socket connection with Google's DNS server.
    If successful, it implies an active internet connection.
    
    :param host: The host IP to connect to for checking the internet connection.
    :param port: The port number to use for the connection.
    :param timeout: Connection timeout in seconds.
    :return: True if the internet connection is available, False otherwise.
    """
    try:
        # Use the socket to attempt to connect to the host
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error as ex:
        print(f"No internet connection: {ex}")
        return False

def main():
    print("Waiting for internet connection...")

if __name__ == "__main__":
    main()
