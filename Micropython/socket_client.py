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

 
def connect_websocket(server_address, port):
    # Connect to the server
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    addr = socket.getaddrinfo(server_address, port)[0][-1]
    s.connect(addr)
 
    # Perform WebSocket handshake
    s.send(b'GET / HTTP/1.1\r\n'
           b'Host: ' + server_address.encode() + b'\r\n'
           b'Upgrade: websocket\r\n'
           b'Connection: Upgrade\r\n'
           b'Sec-WebSocket-Key: ' + b'12345678' + b'\r\n'  # Use a random key
           b'Sec-WebSocket-Version: 13\r\n'
           b'\r\n')
 
    # Verify handshake response
    response = s.recv(4096)
    print(response)
    if not response.startswith(b'HTTP/1.1 101'):
        print("Failed to establish WebSocket connection")
        return None
 
    return s
 
def send_message(socket, message):
    # Encode message according to WebSocket framing
    message = message.encode('utf-8')
    message_length = len(message)
    encoded_message = bytearray()
    encoded_message.append(0x81)  # Text frame (FIN bit set)
    if message_length <= 125:
        encoded_message.append(message_length)
    elif message_length <= 65535:
        encoded_message.append(126)
        encoded_message.extend(struct.pack('>H', message_length))
    else:
        encoded_message.append(127)
        encoded_message.extend(struct.pack('>Q', message_length))
    encoded_message.extend(message)
    print("enc_mess:", encoded_message)
    print("len",len(encoded_message))
    # Send the encoded message
    socket.send(encoded_message)
 
def receive_message(socket):
    # Receive and decode message
    data = socket.recv(4096)
    print("data: ",data)
    if data:
        opcode = data[0] & 0x0F
        if opcode == 0x08:  # Connection close
            return None
        if opcode == 0x01:  # Text frame
            payload_length = data[1] & 0x7F
            if payload_length <= 125:
                payload_start = 2
            elif payload_length == 126:
                payload_start = 4
            else:
                payload_start = 10
            payload = data[payload_start:]
            return payload.decode('utf-8')
    return None
 
# Test the WebSocket client
def main():
    server_address = "192.168.1.165"
    port = 8080
 
    websocket = connect_websocket(server_address, port)
    if websocket:
        print("sending msg")
        send_message(websocket, "Hello, server!")
        print("sent msg")
        response = receive_message(websocket)
        if response:
            print("Received from server:", response)
        else:
            print("Connection closed by server")
        websocket.close()
    else:
        print("Failed to establish connection")
 
connect_to_wifi()
main()