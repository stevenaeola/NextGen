from picounicorn import PicoUnicorn
picounicorn = PicoUnicorn()

import os
import usocket as socket
import ustruct as struct
import network
import ure

def circle(x,y,r,g,b,radius=1):
    for i in range(floor(-radius), ceil(radius+1)):
        for j in range(floor(-radius), ceil(radius+1)):
            if i**2 + j**2 <= (radius*1.5)**2:
                f = ((radius*1.5)**2 - i**2 - j**2)/((radius*1.5)**2)
                f=f**1.5
                print(f)
                picounicorn.set_pixel(x+i,y+j,floor(r*f),floor(g*f),floor(b*f))
            if i**2 + j**2 <= (radius*0.75)**2:
                picounicorn.set_pixel(x+i,y+j,r,g,b)
                
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
SERVER_ADDRESS = '192.168.1.177'
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
    print("message:",request)
    key = parse_websocket_header(request)
    if key == None:
        key = bytes("", 'utf-8')
    print("key:",key)
    # Generate WebSocket accept key
    accept_key = generate_websocket_accept(key)

    # Send the WebSocket handshake response
    #response = b"HTTP/1.1 101 Switching Protocols\r\n"
    #response += b"Upgrade: websocket\r\n"
    #response += b"Connection: Upgrade\r\n"
    #response += b"Sec-WebSocket-Accept: " + accept_key + b"\r\n\r\n"
    #client.send(response)

    response = web_page()
    client_socket.send("HTTP/1.1 200 OK\n")
    client_socket.send("Content-Type: text/html\n")
    client_socket.send("Connection: close\n\n")
    client_socket.sendall(response)
    
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

# Variable to store the current arrow clicked
current_arrow = {'direction': None}

# HTML content for the webpage
html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Arrow Buttons</title>
    <style>
        body {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            background-color: #f0f0f0;
            font-family: Arial, sans-serif;
        }
        .container {
            text-align: center;
        }
        .arrow-buttons {
            display: flex;
            justify-content: center;
            margin-bottom: 20px;
        }
        .arrow-button {
            width: 60px;
            height: 60px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 10px;
            border: 2px solid #333;
            border-radius: 10px;
            background-color: #fff;
            font-size: 24px;
            cursor: pointer;
            user-select: none;
        }
        .arrow-button:hover {
            background-color: #ddd;
        }
        .output {
            font-size: 24px;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="arrow-buttons">
            <div class="arrow-button" onclick="sendArrow('Up')">↑</div>
            <div class="arrow-button" onclick="sendArrow('Left')">←</div>
            <div class="arrow-button" onclick="sendArrow('Right')">→</div>
            <div class="arrow-button" onclick="sendArrow('Down')">↓</div>
        </div>
        <div class="output" id="output">Click an arrow</div>
    </div>

    <script>
        function sendArrow(direction) {
            fetch(`/set_arrow/${direction}`, { method: 'POST' })
                .then(response => response.json())
                .then(data => {
                    console.log('Arrow clicked:', direction);
                    updateCurrentArrow();
                });
        }

        function updateCurrentArrow() {
            fetch('/get_arrow')
                .then(response => response.json())
                .then(data => {
                    const output = document.getElementById('output');
                    output.innerText = data.direction ? `Current arrow clicked: ${data.direction}` : 'Click an arrow';
                });
        }

        // Initial call to set the output on page load
        updateCurrentArrow();
    </script>
</body>
</html>
"""

# Function to handle HTTP requests
def handle_request(client_socket):
    global current_arrow
    request = client_socket.recv(1024)
    request_str = str(request)
    
    if 'GET / ' in request_str:
        response = html
        content_type = 'text/html'
    elif 'POST /set_arrow/' in request_str:
        match = ure.search('/set_arrow/(\w+)', request_str)
        if match:
            current_arrow['direction'] = match.group(1)
        response = '{"status": "success"}'
        content_type = 'application/json'
    elif 'GET /get_arrow' in request_str:
        response = '{"direction": "' + (current_arrow['direction'] if current_arrow['direction'] else '') + '"}'
        content_type = 'application/json'
    else:
        response = '404 Not Found'
        content_type = 'text/plain'
    
    client_socket.send('HTTP/1.1 200 OK\r\nContent-Type: ' + content_type + '\r\n\r\n')
    client_socket.send(response)
    client_socket.close()

connect_to_wifi()
# Create a TCP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_ADDRESS, SERVER_PORT))
server_socket.listen(1)
print("WebSocket server listening on", SERVER_ADDRESS, "port", SERVER_PORT)

while True:
    client_socket, client_address = server_socket.accept()
    handle_request(client_socket)    
    print(current_arrow)
    #response = web_page()
    #client_socket.send("HTTP/1.1 200 OK\n")
    #client_socket.send("Content-Type: text/html\n")
    #client_socket.send("Connection: close\n\n")
    #client_socket.sendall(response)
    #client_socket.close()
