from socket import *
from threading import *
import os
import datetime
import time
localhost = '127.0.0.1'    #서버의 IP address
port = 8888         #사용할 포트 번호
def print_time():     #현재 시간을 나타내는 함수
    current_time = datetime.datetime.now().strftime('[%H:%M]')    #(ex) 21:38
    return current_time
def send(): #Send와 Recv으로 함수를 나누는 생각은 https://hyobn.tistory.com/15?category=906079에서 참조하였음
    while True:
        send_data = input('')
        client_sock.send(send_data.encode('utf-8'))
        if send_data == '!quit':
            client_sock.send(name.encode('utf-8'))
            print('연결을 종료하였습니다.')
            break
    client_sock.close()
    os._exit(1)
def receive(): #Send와 Recv으로 함수를 나누는 생각은 https://hyobn.tistory.com/15?category=906079에서 참조하였음
    while True:
        try:
            recv_data = (client_sock.recv(1024)).decode('utf-8')
            if len(recv_data) == 0:
                print('서버와의 연결이 끊어졌습니다.')
                client_sock.close()
                os._exit(1)
        except Exception as e:
            print('메시지를 수신하지 못하였습니다.')
        else:
            print(recv_data)
            pass
client_sock = socket(AF_INET, SOCK_STREAM)
try:
    client_sock.connect((localhost, port))
except ConnectionRefusedError:      #서버에 접속하지 못하였을 떄 출력되는 메세지
    print('서버에 연결할 수 없습니다.')
    os._exit(1)
except:
    print('프로그램을 실행할 수 없습니다.')
else:
    print('서버와 연결되었습니다.')
while True:
    print('닉네임을 입력하세요:')
    name = input()
    client_sock.send(name.encode())
    is_possible_name = client_sock.recv(1024).decode()      #닉네임을 입력하였을 때 기존에 존재하던 닉네임일 경우 다시 입력하도록 한다.
    if is_possible_name == 'yes':
        print(print_time() + '채팅방에 입장하였습니다.')
        client_sock.send('!enter'.encode())
        break
    elif is_possible_name == 'overlapped':
        print('사용중인 이름입니다.')
sender = Thread(target=send, args=())   #Thread하는 방법은 https://watchout31337.tistory.com/117에서 참조
receiver = Thread(target=receive, args=())
sender.start()
receiver.start()
while True:
    time.sleep(1)
    pass
client_sock.close()