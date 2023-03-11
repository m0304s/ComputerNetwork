from socket import *
# import webbrowser module to open the file as web browser
import webbrowser
# Prepare a client socket
serverName = '127.0.0.1'
serverPort = 6789
# filename = '/HelloWorld.html'
filename = '/Users/choeminseok/PycharmProjects/Computer_Network_Socket_Programming/HelloWorld.html'

# use Ipv4, TCP protocol
clientSocket = socket(AF_INET, SOCK_STREAM)
# request connection to server
clientSocket.connect((serverName, serverPort))
# http method : GET, Host: 127.0.0.1/12345
request = 'GET %s %s %s' %(filename, serverName, serverPort)
# send request to server
clientSocket.send(request.encode())
# receive message from server through socket
result = clientSocket.recv(65535)
status = int(result.decode().split('\n')[0].split(' ')[1])
# create html file received from server only http status is 200.
if (status == 200) :
    htmlResponse = ''
    for i in result.decode().split('\n')[1:]:
        htmlResponse += i
    filepath = 'response.html'
    with open(filepath, 'w') as f:
        f.write(htmlResponse)
        f.close()
    # open web browser with received html file
    webbrowser.open_new_tab(filepath)
# print http status line
print(result.decode().split('\n')[0])
# close socket
clientSocket.close()