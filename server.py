import socket
import select

HEADER_LENGTH = 10
IP = "127.0.0.1"
PORT = 1234

server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_sock.bind((IP, PORT))

server_sock.listen()

sockets_list = [server_sock]

clients = {}

def receive_msg(client_sock):
    try:
        msg_header = client_sock.recv(HEADER_LENGTH)

        if not len(msg_header):
            return False
        
        msg_length = int(msg_header.decode('utf-8').strip())
        return {'header': msg_header, 'data': client_sock.recv(msg_length)}

    except:
        return False


while True:
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)

    for notified_sock in read_sockets:
        if notified_sock == server_sock:
            client_sock, client_addr = server_sock.accept()

            user = receive_msg(client_sock)
            if user is False:
                continue
            sockets_list.append(client_sock)
            clients[client_sock] = user

            print(f"{user['data'].decode('utf-8')} has connected from: {client_addr[0]}:{client_addr[1]}")
        else:
            msg = receive_msg(notified_sock)

            if msg is False:
                print(f"closed connection")
                sockets_list.remove(notified_sock)
                del clients[notified_sock]
            
        
            user = clients[notified_sock]
            print(f"Recieved message from {user['data'].decode('utf-8')}: {msg['data'].decode('utf-8')}")

            for client_sock in clients:
                if client_sock != notified_sock:
                    client_sock.send(user['header'] + user['data'] + msg['header'] + msg['data'])

    for notified_sock in exception_sockets:
        sockets_list.remove(notified_sock)
        del clients[notified_sock]