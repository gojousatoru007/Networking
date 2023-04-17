# Networking

## Socket Programming

Harsh Tomar (B21AI049) &
Aradhya Patel (B21AI050)


In this assignment, we will build a simple client-server system, where you use the client to chat with a "Math" server. The protocol between the client and server is as follows:

- The server is first started on a known port.

- The client program is started (Server IP and port is provided on the commandline).

- The client connects to the server, and then asks the user for input. The user enters a simple arithmetic expression string (e.g., "1+2", "5 - 6", "3 * 4"). The user's input is sent to the server via the connected socket.

- The server reads the user's input from the client socket, evaluates the expression, and sends the result back to the client

- The client should display the server's reply to the user, and prompt the user for the next input, until the user terminates the client program with Ctrl+C.



## The Servers

**Part 1: Single Process Server (8 Marks)**

The server serves one client at a time, meanwhile if any other client tries to access the server, they get the Server Busy error message.

### Deployment

To deploy this server run

```bash
  python server1.py
```
You will be asked for a server host ip address (The Host IP Address for your server):

We can use local host as our host ip address but since we will use Multiple VM's to run as client, it's better to use our Wi-Fi IP Address so that we are on the same network as our VM's (Depending on the Network Configuration of the VMs)

Go To Your Terminal and run

```bash
ipconfig
```
If you are on Linux (Arch Linux):
```bash
ip address show
```
or
```bash
ip a s
```
will work!

You might see something like this:
```bash
Wireless LAN adapter Wi-Fi:

   Connection-specific DNS Suffix  . :
   Link-local IPv6 Address . . . . . : fe80::9f1f:d61f:3b31:1120%18
   IPv4 Address. . . . . . . . . . . : 172.31.27.135
   Subnet Mask . . . . . . . . . . . : 255.255.192.0
   Default Gateway . . . . . . . . . : 172.31.0.1
```
Choose the IP Address that corresponds to the Network Adapter, in our case (IIT Jodhpur Wi-Fi), we have 172.31.27.135

```bash
Enter Host IP Address: 172.31.27.135 
```
Enter the Port Number that you want to deploy your server on!
```bash
Enter the known Port Number: 5000
```

The server will be deployed and listening on the given port!

```bash
Math Server Started On 172.31.27.135:5000
```




### Deploying The Client and Getting Answers from the Server

Since we have a client.c already!
If you are on linux, compile the client.c into client or a.out

```bash
gcc -o client client.c -lws2_32
```

If you are on windows, I have added a client_windows.c as well

```bash
gcc -o client client_windows.c -lws2_32 
```

To Run the client and connect with the socket, we have to pass the Host IP and Port Number as the arguements

```bash
./client 172.31.27.135 5000
```

Will lead to

```bash
Connected to server!
Please enter the message to the server:
```

From here on you can ask math queries and the server will reply

**Example**
```bash
Please enter the message to the server: 3 * 3
Server Replied: 9
```

### To Produce the Server Busy Error
Repeat the steps and deploy another client on another terminal and try to ask something from the server!

```bash
Server replied: Server is busy. Please wait.
```




***Part 2: Multi-Process / Multi-Threaded Server (12 Marks)**

The server can serve multiple clients at the same time.


### Deployment

To deploy this server run

```bash
  python server2.py
```
You will be asked for a server host ip address (The Host IP Address for your server):

We can use local host as our host ip address but since we will use Multiple VM's to run as client, it's better to use our Wi-Fi IP Address so that we are on the same network as our VM's (Depending on the Network Configuration of the VMs)

Go To Your Terminal and run

```bash
ipconfig
```
If you are on Linux (Arch Linux):
```bash
ip address show
```
or
```bash
ip a s
```
will work!

You might see something like this:
```bash
Wireless LAN adapter Wi-Fi:

   Connection-specific DNS Suffix  . :
   Link-local IPv6 Address . . . . . : fe80::9f1f:d61f:3b31:1120%18
   IPv4 Address. . . . . . . . . . . : 172.31.27.135
   Subnet Mask . . . . . . . . . . . : 255.255.192.0
   Default Gateway . . . . . . . . . : 172.31.0.1
```
Choose the IP Address that corresponds to the Network Adapter, in our case (IIT Jodhpur Wi-Fi), we have 172.31.27.135

```bash
Enter Host IP Address: 172.31.27.135 
```
Enter the Port Number that you want to deploy your server on!
```bash
Enter the known Port Number: 5000
```

The server will be deployed and listening on the given port!

```bash
Math Server Started On 172.31.27.135:5000
```

### Deploying Multiple Client and Getting Answers from the Server

Since we have a client.c already!
If you are on linux, compile the client.c into client or a.out

```bash
gcc -o client client.c -lws2_32
```

If you are on windows, I have added a client_windows.c as well

```bash
gcc -o client client_windows.c -lws2_32 
```

To Run the client and connect with the socket, we have to pass the Host IP and Port Number as the arguements

```bash
./client 172.31.27.135 5000
```

Will lead to

```bash
Connected to server!
Please enter the message to the server:
```

From here on you can ask math queries and the server will reply

**Example**
```bash
Please enter the message to the server: 3 * 3
Server Replied: 9
```

### We can use multiple clients to get the answers and the server will reply to all of them at the same time
Repeat the steps and deploy another client on another terminal and try to ask something from the server!




