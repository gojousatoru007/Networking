
import signal
import sys
import socket
import threading
import queue

class MathServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_queue = queue.Queue()
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
                # Add the client to the queue
                self.lock.acquire()
                self.client_queue.put(client_socket)
                self.lock.release()

                # Check if the client is at the front of the queue
                self.lock.acquire()
                is_front = self.client_queue.queue[0] is client_socket
                self.lock.release()

                # Send busy server message to other clients
                if not is_front:
                    self.lock.acquire()
                    self.client_queue.queue.remove(client_socket)
                    self.lock.release()
                    #self.client_queue.queue.remove(client_socket)
                    print(len(self.client_queue.queue))
                    client_socket.sendall(b"Server is busy. Please wait.\n")
                    
                    client_socket.close()
                    break

                # Receive input from the client
                data = client_socket.recv(1024).decode().strip()

                if data.lower() == "disconnect":
                    # Remove the client from the queue if it sends the disconnect command
                    self.lock.acquire()
                    self.client_queue.queue.remove(client_socket)
                    self.lock.release()
                    break

                # Process the math request
                result = self.process_math_request(data)
                print(f"Client Socket {client_socket.getpeername()[1]} sent message: {data}")


                # Send the result back to the client
                client_socket.sendall(str(result).encode() + b"\n")
                print(f"Sending reply: {result}")

        except ConnectionResetError:
            # Client disconnected unexpectedly
            self.lock.acquire()
            if client_socket in self.client_queue.queue:
                self.client_queue.queue.remove(client_socket)
            self.lock.release()

        finally:
            # Remove the client from the queue if it's still in there
            self.lock.acquire()
            if client_socket in self.client_queue.queue:
                self.client_queue.queue.remove(client_socket)
            self.lock.release()

            # Close the client socket
            client_socket.close()
            self.lock.acquire()
            if client_socket in self.client_queue.queue:
                self.client_queue.queue.remove(client_socket)
            self.lock.release()
            #self.client_queue.queue.remove(client_socket)
            print(len(self.client_queue.queue))
            print("Client disconnected")

    # this is the self implemented code to perform operations between two operands
    # def process_math_request(self, request):
    #     try:
    #         parts = request.split()
    #         num1 = Decimal(parts[0])
    #         num2 = Decimal(parts[2])
    #         operator = parts[1]
    #         if operator == "+":
    #             return num1 + num2
    #         elif operator == "-":
    #             return num1 - num2
    #         elif operator == "*":
    #             return num1 * num2
    #         elif operator == "/":
    #             return num1 / num2
    #         else:
    #             return "Invalid operator"
    #     except:
    #         return "Invalid input"

    def process_math_request(self, request):
        try:
            result = eval(request)
            return result
        except:
            return "Invalid input"



if __name__ == "__main__":
    host = str(input("Enter Host IP Address: "))
    port = int(input("Enter the known port number: "))
    
    math_server = MathServer(host, port)
    math_server.start()

