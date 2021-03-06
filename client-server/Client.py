import socket
import time

from lib.KeyListen import *
from lib.ANSI import *
from lib.UDP import resolve_offer

UDP_PORT = 13117
BUFF_SIZE = 1024
PLAYER_NAME = "Ninja\n"

if __name__ == '__main__':
    keyboard_listener = KBHit()
    # Creating a UDP socket for server offers.
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    client_socket.bind(("", UDP_PORT))

    print(bold() + italic() + color_green()
          + "Client started, listening for offer requests..." + reset())

    # Getting the server's broadcast offer.
    while True:
        try:
            data, address = client_socket.recvfrom(BUFF_SIZE)
            tcp_port = resolve_offer(data)
            host_name = address[0]
            print(tcp_port)
            print(color_green() + f"Received offer from {address} ,"
                  + italic() + " attempting to connect..." + reset())
            client_socket.close()

            # Creating a TCP socket and connect to the server.
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.connect((host_name, tcp_port))
            print(f"Connected successfully to {host_name}:{tcp_port} !")

            # Sending player name to server.
            # PLAYER_NAME = input("ENTER NAME:")
            server_socket.sendall(PLAYER_NAME.encode())

            # Receiving question from server.
            question = server_socket.recv(BUFF_SIZE).decode()
            print(question)

            end_time = time.time() + 10

            ANSWERED = False

            while end_time > time.time():
                if keyboard_listener.kbhit():
                    # Sending answer to server.
                    answer = keyboard_listener.getch()
                    print(f"You Answered: {answer}")
                    server_socket.sendall(answer.encode())
                    ANSWERED = True
                    break 

            # Receiving results from server.
            results = server_socket.recv(BUFF_SIZE).decode()
            print(results)

        except Exception as e:
            print_error(e)
            break
