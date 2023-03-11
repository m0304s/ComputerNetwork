#큐를 사용해서 사용자들의 정보를 받아오는 생각은 https://hyobn.tistory.com/15?category=906079에서 참조하였음
from socket import*
from threading import *
from queue import *
import sys
import datetime

if len(sys.argv) <= 1:
    print('Usage : Server IP address PORT NUMBER')
    sys.exit(2)
localhost = sys.argv[1]    #서버의 IP address
PORT = sys.argv[2]         #사용할 포트 번호

# localhost = '127.0.0.1'    #서버의 IP address
# PORT = 8888         #사용할 포트 번호

def print_time():     #현재 시간을 나타내는 함수
    time = datetime.datetime.now()
    current_time = time.strftime('[%H:%M]')    #(ex) 21:38
    return current_time

def send(lock): #Send와 Recv으로 함수를 나누는 생각은 https://hyobn.tistory.com/15?category=906079에서 참조하였음
    while True:
        try:
            received = received_msg_info.get()  #get을 사용해서 큐에서 제거
            if received[0] == '!enter' or received[0] == '!member':   #사용자가 들어왔을 경우 전송하는 메세지
                now_member_msg = '현재 멤버: '
                for mem in member_name_list:
                    if mem != '-1': #연결을 종료한 클라이언트가 아닌 경우
                        now_member_msg += '['+mem+'] '
                # received[1].send(now_member_msg.encode())
                if(received[0] == '!enter'):
                    msg = str(print_time() + member_name_list[received[2]]) + '님이 입장하였습니다.'
                else:
                    received[1].send(now_member_msg.encode())
                    continue
            elif received[0] == '!quit':     #연결을 종료하였을 시 전송하는 메세지
                msg = print_time() + left_member_name + '님이 연결을 종료하였습니다.'
            elif received[0].find('/w') == 0:     #귓속말 기능은 https://lcodea.tistory.com/21 에서 참조
                split_msg = received[0].split()
                if split_msg[1] in member_name_list:
                    msg = print_time()+'(귓속말)'+member_name_list[received[2]]+':'
                    msg = msg+received[0][len(split_msg[1])+4:len(received[0])]
                    idx = member_name_list.index(split_msg[1])
                    socket_descriptor_list[idx].send(msg.encode())
                else:
                    msg = '해당 사용자가 존재하지 않습니다.'
                    received[1].send(msg.encode())
                continue
            else:
                msg = print_time() + member_name_list[received[2]] + ' : ' + received[0]
            for conn in socket_descriptor_list:
                if conn == '-1':  # 연결 종료한 클라이언트 경우.
                    continue
                else:
                    conn.send(msg.encode())
                    pass
            if received[0] == '!quit':
                received[1].close()
        except:
                pass

def receive(conn, count, lock): #Send와 Recv으로 함수를 나누는 생각은 https://hyobn.tistory.com/15?category=906079에서 참조하였음
    if socket_descriptor_list[count] == '-1':
        return -1
    while True:
        global left_member_name
        data = conn.recv(1024).decode()
        received_msg_info.put([data, conn, count])  #put을 사용해서 큐에 추가
        if data == '!quit' or len(data) == 0:
            lock.acquire()      #스레드를 사용할때 lock하는 방법은 https://hyobn.tistory.com/32에서 참조
            print(print_time() + member_name_list[count] + '님이 연결을 종료하였습니다.')
            left_member_name = member_name_list[count]
            socket_descriptor_list[count] = '-1'
            for i in range(len(whisper_list)):
                if whisper_list[i] == count:
                    whisper_list[i] = -1
            member_name_list[count] = '-1'
            lock.release()      #스레드를 사용할때 lock하는 방법은 https://hyobn.tistory.com/32에서 참조
            break
    conn.close()

print(print_time()+'서버를 시작합니다.')
server_sock = socket(AF_INET, SOCK_STREAM)
server_sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)   #Already used address 에러 방지하는 방법은 https://snowdeer.github.io/c++/2017/08/17/setsockopt/에서 참조
server_sock.bind((localhost, int(PORT)))
server_sock.listen()
count = 0
socket_descriptor_list = ['-1', ]  # 클라이언트들의 소켓 디스크립터 저장하는 방법은 https://hyobn.tistory.com/15?category=906079에서 참조
member_name_list = ['-1', ]  # 클라이언트들의 닉네임 저장
whisper_list = [-1, ]
received_msg_info = Queue()
left_member_name = ''
lock = Lock()                   #스레드를 사용할때 lock하는 방법은 https://hyobn.tistory.com/32에서 참조
while True:
    count = count+1     #현재 연결된 client의 count
    conn, addr = server_sock.accept()
    while True:
        client_name = conn.recv(1024).decode()
        if not client_name in member_name_list:
            conn.send('yes'.encode())
            break
        else:
            conn.send('overlapped'.encode())
    member_name_list.append(client_name)
    socket_descriptor_list.append(conn)
    print(print_time()+client_name+'님이 연결되었습니다. 연결 IP: '+addr[0])

    sender = Thread(target=send, args=(lock,))
    sender.start()
    receiver = Thread(target=receive, args=(conn,count,lock))
    receiver.start()
server_sock.close()
