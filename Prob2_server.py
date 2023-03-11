from socket import *
import sys

if len(sys.argv) <= 1:
    print('Usage : "python ProxyServer.py server_ip"\n[server_ip : It is the IP Address Of Proxy Server')
    sys.exit(2)

# Create a server socket, bind it to a port and start listening
tcpSerSock = socket(AF_INET, SOCK_STREAM)
# Fill in start.
localhost = sys.argv[1]
ServerPort = 8888
tcpSerSock.bind((localhost, ServerPort))
tcpSerSock.listen(5)
# Fill in end.
while 1:
    # Start receiving data from the client
    print('Ready to serve...')
    tcpCliSock, addr = tcpSerSock.accept()
    print('Received a connection from:', addr)
    # Fill in start.
    message = tcpCliSock.recv(1024).decode()
    # Fill in end.
    print(message)
    # Extract the filename from the given message
    # print(message.split()[1])
    filename = message.split()[1].partition("/")[2]
    # print("FileName=", filename)
    fileExist = "false"
    filetouse = "/" + filename
    # print('FileTouse=', filetouse)
    try:
        # Check wether the file exist in the cache
        f = open(filetouse[1:], "rb")
        outputdata = f.readlines()
        fileExist = "true"
        # ProxyServer finds a cache hit and generates a response message
        for i in range(0, len(outputdata)):
            tcpCliSock.send(outputdata[i])
        # Fill in end.
        print('Read from cache')
    # Error handling for file not found in cache
    except IOError as e:
        # print(str(e))
        if fileExist == "false":
            # Create a socket on the proxy server
            c = socket(AF_INET, SOCK_STREAM)
            hostn = filename.replace("www.", "", 1)
            # print('hostn=', hostn)
            try:
                # Connect to the socket to port 80
                c.connect((hostn, 80))
                # Create a temporary file on this socket and ask port 80 for the file requested by the client
                fileobj = c.makefile('rwb', 0)
                new_file = "GET " + "http://" + filename + " HTTP/1.0\n\n"
                fileobj.write(new_file.encode())
                # Read the response into buffer
                buffer = fileobj.readlines()
                # Create a new file in the cache for the requested file.
                # Also send the response in the buffer to client socket and the corresponding file in the cache
                tmpFile = open("./" + filename, "wb")
                for i in range(0, len(buffer)):
                    tmpFile.write(buffer[i])
                    tcpCliSock.send(buffer[i])
            except Exception as e:
                print(str(e))
                print("Illegal request")
                break
    else:
        # HTTP response message for file not found
        print('404 File Not Found')
        # Close the client and the server sockets
        tcpCliSock.close()
tcpSerSock.close()