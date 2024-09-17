from picounicorn import PicoUnicorn
import time
import random
from math import floor, ceil
picounicorn = PicoUnicorn()
buttonpress = False
button = None

import os
import usocket as socket
import ustruct as struct
import network
import ure


h = picounicorn.get_width()
w = picounicorn.get_height()

red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
black = (0,0,0)
white = (255,255,255)


m = [[0,0,0,0,0,0,0],[0,0,0,1,0,0,0],[0,0,0,1,0,0,0],[0,0,1,1,1,0,0],[0,1,1,1,1,1,0],[1,1,1,1,0,1,0],[1,0,1,1,0,1,0],[1,0,1,1,0,1,1],[1,0,1,1,0,0,0],[0,0,1,1,0,0,0],[0,0,1,1,0,0,0],[0,1,1,0,1,0,0],[0,1,0,0,1,1,0],[1,1,0,0,1,1,0],[1,0,0,0,0,1,1],[0,1,0,0,0,1,0]]
pause = 3
def clear():
    picounicorn.clear()
    
    
def draw_rectangle(x1,y1,x2,y2,colour):
    (r,g,b) = colour
    for i in range(x1,x2+1):
        for j in range(y1,y2+1):
            picounicorn.set_pixel(i,j,r,g,b)
    
def draw_square(x1,y1,size,colour):
    draw_rectangle(x1,y1,x1+size-1,y1+size-1,colour)
    
def draw_circle(x,y,radius,colour):
    (r,g,b) = colour
    for i in range(floor(-radius), ceil(radius+1)):
        for j in range(floor(-radius), ceil(radius+1)):
            if i**2 + j**2 <= (radius*1.5)**2 and 0<= x+i and 0 <= y+j and x+i <= 15 and y+j <= 6:
                f = ((radius*1.5)**2 - i**2 - j**2)/((radius*1.5)**2)
                f=f**1.5
                picounicorn.set_pixel(x+i,y+j,floor(r*f),floor(g*f),floor(b*f))
            if i**2 + j**2 <= (radius*0.75)**2:
                picounicorn.set_pixel(x+i,y+j,r,g,b)
    
def wait_button():
    while True:
        if picounicorn.is_pressed(picounicorn.BUTTON_A):
            return "A"
        if picounicorn.is_pressed(picounicorn.BUTTON_B):
            return "B"
        if picounicorn.is_pressed(picounicorn.BUTTON_X):
            return "X"
        if picounicorn.is_pressed(picounicorn.BUTTON_Y):
            return "Y"
    

def wait_time(t):
    future = time.time()+t
    while time.time()<future:
        ...
    
def wait_time_button(t):
    future = time.time()+t
    while time.time()<future:
        if picounicorn.is_pressed(picounicorn.BUTTON_A):
            return True
        if picounicorn.is_pressed(picounicorn.BUTTON_B):
            return True
        if picounicorn.is_pressed(picounicorn.BUTTON_X):
            return True
        if picounicorn.is_pressed(picounicorn.BUTTON_Y):
            return True
    return False

def update_ball_position(x,y):
    
    return x,y

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
        .arrow-button.active {
            background-color: #ddd;
            border-color: #000;
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
            <div id="up" class="arrow-button" onclick="sendArrow('Up')">↑</div>
            <div id="left" class="arrow-button" onclick="sendArrow('Left')">←</div>
            <div id="right" class="arrow-button" onclick="sendArrow('Right')">→</div>
            <div id="down" class="arrow-button" onclick="sendArrow('Down')">↓</div>
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
                    const direction = data.direction;
                    output.innerText = direction ? `Current arrow clicked: ${direction}` : 'Click an arrow';

                    // Remove 'active' class from all buttons
                    document.querySelectorAll('.arrow-button').forEach(button => {
                        button.classList.remove('active');
                    });

                    // Add 'active' class to the corresponding button
                    if (direction) {
                        document.getElementById(direction.toLowerCase()).classList.add('active');
                    }
                });
        }

        function handleKeyDown(event) {
            const keyMap = {
                ArrowUp: 'Up',
                ArrowLeft: 'Left',
                ArrowRight: 'Right',
                ArrowDown: 'Down'
            };

            const direction = keyMap[event.code];
            if (direction) {
                sendArrow(direction);
                event.preventDefault(); // Prevent default scrolling behavior
            }
        }

        window.addEventListener('keydown', handleKeyDown);

        // Initial call to set the output on page load
        updateCurrentArrow();
    </script>
</body>
</html>
"""

# Function to handle HTTP requests
def handle_request(client_socket,func):
    global current_arrow
    request = client_socket.recv(1024)
    request_str = str(request)
    
    if 'GET / ' in request_str:
        response = html
        content_type = 'text/html'
    elif 'POST /set_arrow/' in request_str:
        match = ure.search('/set_arrow/(\w+)', request_str)
        if match:
            func(match.group(1))
        response = '{"status": "success"}'
        content_type = 'application/json'
    else:
        response = '404 Not Found'
        content_type = 'text/plain'
    
    client_socket.send('HTTP/1.1 200 OK\r\nContent-Type: ' + content_type + '\r\n\r\n')
    client_socket.send(response)
    client_socket.close()
    
def setup_server(func):
    connect_to_wifi()
    # Create a TCP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_ADDRESS, SERVER_PORT))
    server_socket.listen(1)
    while True:
        client_socket, client_address = server_socket.accept()
        handle_request(client_socket,func)

