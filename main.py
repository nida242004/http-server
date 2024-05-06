import socket

SERVER_HOST = "0.0.0.0"
SERVER_PORT = 8080

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #tcp SOCK_DGRAM ->udp
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #this line lets the server socket to reuse the local adress immediately after its closed
#server_socket.setblocking(False) #it wont block untill a connection becomes available

server_socket.bind((SERVER_HOST, SERVER_PORT)) #127.0.0.1->only from this device #port 0-1023 are reserved for OS

server_socket.listen(5) #size of queue 

print(f"listening on port {SERVER_PORT}...")

# while True: #go on trying untill there is a connection req
#     try: # using try because when queue is 0 it shd block
#         client_socket, client_address = server_socket.accept() #accepts the first queue element ka tuple of socket and address
#         print(client_address)
#         print(client_socket)
#     except:
#         time.sleep(1)
#         continue  
# this while block makes the server load continously bcz theres no request

while True: #go on trying untill there is a connection req
    client_socket, client_address = server_socket.accept() #accepts the first queue element ka tuple of socket and address
    request = client_socket.recv(1500).decode() #max amt of data is buffsize   
    print(request)   
    headers = request.split('\n') 
    print(headers[0]) #get / http/1.1
    first_header_components = headers[0].split()
    http_method = first_header_components[0] #get
    path = first_header_components[1] #/


    if http_method == 'GET':
        if path == '/': #home page
            fin = open('index.html')
            content = fin.read()
        elif path == '/book':
            fin = open('book.json')
            content = fin.read()
        else:
            content = '404 Not Found'

        # structure of http response:
        # STATUS LINE - VERSION, STATUS CODE , OPTIONAL TEXT MSG REGARDING STATUS
        # HEADERS - similar to http (optional)
        # MESSAGE BODY - msg body (optional)

        fin.close() 
        response = 'HTTP/1.1 200 OK\n\n' + content #200:everything went well   
    else:
        response = 'HTTP/1.1 405 Method not allowed\n\nAllow: GET'        

    client_socket.sendall(response.encode())
    client_socket.close()    