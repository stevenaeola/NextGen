import usocket as socket
import ustruct as struct

import network

def connect_to_wifi():
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print("Connecting to the network...")
        sta_if.active(True)
        sta_if.connect("robotrouter", "")
        while not sta_if.isconnected():
            pass
    print("Connected with IP: ", sta_if.ifconfig()[0])
    
# Define WebSocket frame opcodes
OPCODE_TEXT = const(0x1)
OPCODE_CLOSE = const(0x8)

# Define WebSocket server address and port
SERVER_ADDRESS = '0.0.0.0'
SERVER_PORT = 8080

def parse_websocket_header(header):
    # Parse WebSocket header and return key
    key = None
    lines = header.split(b'\r\n')
    for line in lines:
        if line.startswith(b'Sec-WebSocket-Key:'):
            key = line.split(b':')[1].strip()
            break
    return key

def generate_websocket_accept(key):
    # Generate WebSocket accept key
    GUID = b'258EAFA5-E914-47DA-95CA-C5AB0DC85B11'
    accept_key = key + GUID
    import hashlib
    import base64
    hashed = hashlib.sha1(accept_key).digest()
    return base64.b64encode(hashed)

def handle_websocket_client(client):
    # Read the first bytes of the request
    request = client.recv(1024)
    key = parse_websocket_header(request)

    # Generate WebSocket accept key
    accept_key = generate_websocket_accept(key)

    # Send the WebSocket handshake response
    response = b"HTTP/1.1 101 Switching Protocols\r\n"
    response += b"Upgrade: websocket\r\n"
    response += b"Connection: Upgrade\r\n"
    response += b"Sec-WebSocket-Accept: " + accept_key + b"\r\n\r\n"
    client.send(response)

    # Start handling WebSocket frames
    while True:
        # Receive WebSocket frame
        frame = client.recv(1024)
        
        if not frame:
            break

        print("This is the frame we've been sent: ",frame)

        # Parse the frame
        opcode = frame[0] & 0x0F
        payload_len = frame[1] & 0x7F

        if opcode == 0x08:  # Connection close
            return None
        if opcode == 0x01:  # Text frame
            if payload_len <= 125:
                mask_offset = 2
            elif payload_len == 126:
                mask_offset = 4
            else:
                mask_offset = 10

        unmasked_data = frame[mask_offset:]

        # Handle frame based on opcode
        if opcode == OPCODE_TEXT:
            print("Received message:", unmasked_data.decode('utf-8'))
            # Echo back the message
            response_frame = bytes([0x81, len(unmasked_data)]) + unmasked_data
            client.send(response_frame)
        elif opcode == OPCODE_CLOSE:
            print("Received close frame")
            # Close the connection
            break

    # Close the client connection
    client.close()

connect_to_wifi()
# Create a TCP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_ADDRESS, SERVER_PORT))
server_socket.listen(1)
print("WebSocket server listening on", SERVER_ADDRESS, "port", SERVER_PORT)

while True:
    # Wait for incoming connections
    client_socket, addr = server_socket.accept()
    print("Client connected from:", addr)
    
    # Handle WebSocket client
    handle_websocket_client(client_socket)
