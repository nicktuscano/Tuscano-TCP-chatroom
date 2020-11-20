import socket
import sys

import select
import errno

HEADER_LENGTH = 10

IP = "127.0.0.1"
PORT = 1234

my_username = input("Enter a username:")
client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_sock.connect((IP, PORT))
client_sock.setblocking(False)

username = my_username.encode('utf-8')
username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
client_sock.send(username_header + username)

while True:
    msg = input(f"{my_username} > ")

    if msg:
        msg = msg.encode('utf-8')
        msg_header = f"{len(msg) :< {HEADER_LENGTH}}".encode('utf-8')
        client_sock.send(msg_header + msg)
    
    try:
        while True:
            #recieve
            username_header = client_sock.recv(HEADER_LENGTH)
            if not len(username_header):
                print("connection closed.")
                sys.exit()
            
            username_length = int(username_header.decode('utf-8').strip())
            username = client_sock.recv(username_length).decode('utf-8')

            msg_header = client_sock.recv(HEADER_LENGTH)
            msg_length = int(msg_header.decode('utf-8').strip())
            msg = client_sock.recv(msg_length).decode('utf-8')

            print(f"{username} > {msg}")

    except IOError as e:
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('READ ERROR', str(e))
            sys.exit()
        continue

    except Exception as e:
        print('ERROR ',str(e))
        sys.exit()