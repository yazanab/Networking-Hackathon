import socket
import threading
import time
from lib.ANSI import *
from lib.UDP import create_offer
from Match import Match

HOST = '0.0.0.0'
TCP_PORT = 2025
UDP_PORT = 13117
BUFF_SIZE = 1024
TIME_OUT = 10
MAX_PLAYERS = 2
BROADCAST_MODE = True
FORMAT = "UTF-8"

clients = []
player_names = []
match = None


def broadcast(_msg):
    try:
        for _client in clients:
            _client_socket = clients[0][0]
            _client_socket.sendall(_msg.encode())
    except Exception as e:
        print_error(e)


def broadcast_to_clients(_udp_socket):
    while len(clients) < MAX_PLAYERS:
        try:
            tcp_port = create_offer(TCP_PORT)
            _udp_socket.sendto(tcp_port, ('<broadcast>', UDP_PORT))
            print(color_cyan() + "Broadcasting . . ." + reset())
            time.sleep(1)
        except Exception as e:
            print_error(e)


if __name__ == '__main__':

    # Creating a TCP socket for the server.
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, TCP_PORT))
    server_socket.listen()

    # Creating a UDP socket for the server in order to broadcast.
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    # Server starting message.
    msg = bold() + italic() + color_green() + "Server started, listening on IP address "
    msg += socket.gethostbyname(socket.gethostname()) + "\n" + reset()
    print(msg)

    while True:  # Server keeps running forever.
        match = Match()

        # Broadcasting, sending offers to clients until the server is full.
        broadcast_thread = threading.Thread(target=broadcast_to_clients, args=[udp_socket])
        broadcast_thread.start()

        while len(clients) < MAX_PLAYERS:

            try:
                # Accepting new client connections.
                client_socket, client_address = server_socket.accept()
                print(color_green() + bold() + f"{client_address} joined to the server!" + reset())

                # Receiving player name from client.
                player_name = client_socket.recv(BUFF_SIZE).decode()
                print(
                    color_green() + bold() + italic() + f"Received player name: {player_name} from {client_address}" + reset())
                player_names.append(player_name)

                # Creating a thread for this client, adding client to clients list.
                client_thread = threading.Thread(target=match.start, args=(client_socket, player_name))
                clients.append((client_socket, client_address, player_name, client_thread))

                if len(clients) == 1:
                    match.add_player1(client_socket, player_name)
                else:
                    match.add_player2(client_socket, player_name)

            except Exception as e:
                print_error(e)

        # Start the match.
        print(color_yellow() + "Broadcast stopped." + reset())
        time.sleep(3)  # TODO: Change later to 10 secs.

        for client in clients:
            thread = client[3]
            thread.start()

        for client in clients:
            thread = client[3]
            thread.join()

        # Clean up client's connections.
        clients = []
        player_names = []

        print("Back to broadcast mode...")
