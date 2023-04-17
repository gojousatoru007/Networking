import signal
import sys
import socket
import threading
from decimal import Decimal
class MathServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.lock = threading.Lock()

    def signal_handler(self, sig, frame):
        print("Stopping Server...")
        self.server_socket.close()
        sys.exit(0)

    def start(self):
        signal.signal(signal.SIGINT, self.signal_handler)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Math Server Started On {self.host}:{self.port}")
        
        try:
            while True:
                client_socket, client_address = self.server_socket.accept()
                print(f"New client connected from {client_address[0]}:{client_address[1]}")
                print(f"Connected with client socket number {client_address[1]}\n")
                
                client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
                client_thread.start()

        except KeyboardInterrupt:
            print("Server Stopped!")    

    def handle_client(self, client_socket):
        try:
            while True:
                # Receive input from the client
                data = client_socket.recv(1024).decode().strip()

                if data.lower() == "disconnect":
                    break

                # Process the math request
                result = self.process_math_request(data)
                print(f"Client Socket {client_socket.getpeername()[1]} sent message: {data}")

                # Send the result back to the client
                client_socket.sendall(str(result).encode() + b"\n")
                print(f"Sending reply: {result}")

        except ConnectionResetError:
            # Client disconnected unexpectedly
            print("Client disconnected unexpectedly")

        finally:
            # Close the client socket
            client_socket.close()
            print("Client disconnected")

    def process_math_request(self, request):
        try:
            parts = request.split()
            num1 = Decimal(parts[0])
            num2 = Decimal(parts[2])
            operator = parts[1]
            if operator == "+":
                return num1 + num2
            elif operator == "-":
                return num1 - num2
            elif operator == "*":
                return num1 * num2
            elif operator == "/":
                return num1 / num2
            else:
                return "Invalid operator"
        except:
            return "Invalid input"


if __name__ == "__main__":
    host = str(input("Enter Host IP Address: "))
    port = int(input("Enter the known port number: "))
    
    math_server = MathServer(host, port)
    math_server.start()
