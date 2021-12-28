import random
import threading
import time

from lib.ANSI import *

TIME_OUT = 10
BUFF_SIZE = 1024


class Match:

    def __init__(self):
        self.__player1_name = ""
        self.__player2_name = ""
        self.__player1_answer = -1
        self.__player2_answer = -1

        self.__thread1 = None
        self.__thread2 = None

        self.__client_socket1 = None
        self.__client_socket2 = None

        clients = []
        player_names = []

        self.__SEND_RES_FLAG = False
        self.__DRAW = True

        self.__real_answer = 0
        self.__equation = ""

        self.__winner_name = ""

        self.__results = "GAME OVER!"

        self.__generate_equation()

    def get_begin_match_msg(self):
        msg = bold() + color_blue() + "\nWelcome to Quick Maths.\n" + reset()
        msg += italic() + "\nPlayer 1: " + self.__player1_name
        msg += italic() + "\nPlayer 2: " + self.__player2_name
        msg += reset() + color_blue() + "\n==\n"
        msg += bold() + color_cyan() + \
            "Please answer the following question as fast as you can:\n" + reset()
        msg += color_yellow() + "How much is " + self.get_math_problem() + " ?\n" + reset()
        return msg

    def start(self, client_socket, player_name):
        print(color_green() + bold() +
              f"\nGAME STARTED NOW for client {player_name} !\n" + reset())

        try:
            print(client_socket)
            # Sends problem to client.
            client_socket.sendall(self.get_begin_match_msg().encode())
            end_time = time.time() + 10
            while (not self.__SEND_RES_FLAG) and (end_time > time.time()):
                # Receiving answers from client.
                answer = client_socket.recv(BUFF_SIZE).decode()
                if not answer:
                    continue
                print(f"Answer received from {player_name}: " + answer)

                if self.__real_answer == int(answer):
                    with threading.Lock():
                        self.__winner_name = player_name
                        self.__SEND_RES_FLAG = True
                        self.__DRAW = False
                    msg = self.get_res()
                    self.__client_socket1.sendall(msg.encode())
                    self.__client_socket2.sendall(msg.encode())
                    break
                else:
                    with threading.Lock():
                        self.__SEND_RES_FLAG = True
                        self.__DRAW = False
                        if player_name != self.__player1_name:
                            self.__winner_name = self.__player1_name
                        else:
                            self.__winner_name = self.__player2_answer
                    msg = self.get_res()
                    self.__client_socket1.sendall(msg.encode())
                    self.__client_socket2.sendall(msg.encode())
                    break

            if self.__DRAW:
                msg = self.get_res()
                with threading.Lock():
                    self.__client_socket1.sendall(msg.encode())
                    self.__client_socket2.sendall(msg.encode())

        except Exception as e:
            print_error(e)

    def get_res(self):
        msg = f"Game Over!\nThe correct answer was {self.__real_answer}!\n\n"
        if self.__winner_name == "":
            msg += "DRAW !"
        else:
            msg += f"Congratulations to the winner: {self.__winner_name}"
        return msg

    def add_player1(self, client_socket, player_name):
        self.__player1_name = player_name
        self.__client_socket1 = client_socket

    def add_player2(self, client_socket, player_name):
        self.__player2_name = player_name
        self.__client_socket2 = client_socket

    def add_player1_answer(self, ans):
        self.__player1_answer = ans

    def add_player2_answer(self, ans):
        self.__player2_answer = ans

    def check_answer(self, answer):
        return self.__real_answer == answer

    def get_math_problem(self):
        return self.__equation

    def get_real_answer(self):
        return self.__real_answer

    def get_results(self):
        return "Game over!\n"

    def __generate_equation(self):
        operator = random.choice(["+", "-", "*"])
        operand1 = random.randint(1, 9)
        operand2 = operand_optional = answer = None
        operator_optional = random.choice(["+", "-", "*", None])

        if operator == "+":
            operand2 = random.randint(0, 9 - operand1)
            answer = operand1 + operand2
        elif operator == "-":
            operand2 = random.randint(0, operand1)
            answer = operand1 - operand2
        elif operator == "*":
            operand2 = random.randint(0, int(9 / operand1))
            answer = operand1 * operand2

        if operator_optional == "+":
            operand_optional = random.randint(0, 9 - answer)
            answer += operand_optional
        elif operator_optional == "-":
            operand_optional = random.randint(0, answer)
            answer -= operand_optional
        elif operator_optional == "*":
            operand_optional = random.randint(
                0, int(9 / answer) if answer != 0 else int(9 / (answer + 1)))
            answer *= operand_optional

        optional = (" " + operator_optional + " " + operand_optional.__str__()
                    ) if operand_optional is not None else ""
        equation = operand1.__str__() + " " + operator + " " + operand2.__str__()
        equation = "(" + equation + ")" + \
            optional if operand_optional is not None else equation

        self.__equation = equation
        self.__real_answer = answer
