import socket

def start_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"Server listening on {host}:{port}")

    while True:
        client_socket, client_addr = server_socket.accept()
        print(f"Connection established with {client_addr[0]}:{client_addr[1]}")

        try:
            # Receive the user query from the client
            user_query = client_socket.recv(1024).decode("utf-8")
            print(f"Received user query: {user_query}")

            # Process the user query here (e.g., send it to OpenAI for processing)
            # Perform the text-to-speech conversion and send the response back to the client

            # Replace the following lines with your TTS implementation for ESP8266
            tts_response = "This is the response from the AI."

            # Send the TTS response back to the client (ESP8266)
            client_socket.sendall(tts_response.encode("utf-8"))
        except Exception as e:
            print(f"Error occurred: {e}")
        finally:
            client_socket.close()

if __name__ == "__main__":
    host = "192.168.159.130"  # Replace this with the IP address of your computer on the local network
    port = 12345  # Choose a port number for communication with ESP8266

    start_server(host, port)
