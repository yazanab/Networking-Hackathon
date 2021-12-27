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

        self.__real_answer = 0
        self.__equation = ""

        self.__results = "GAME OVER!"

    def get_begin_match_msg(self):
        msg = bold() + color_blue() + "\nWelcome to Quick Maths.\n" + reset()
        msg += italic() + "\nPlayer 1: " + self.__player1_name
        msg += italic() + "\nPlayer 2: " + self.__player2_name
        msg += reset() + color_blue() + "\n==\n"
        msg += bold() + color_cyan() + "Please answer the following question as fast as you can:\n" + reset()
        msg += color_yellow() + "How much is " + self.get_math_problem() + " ?\n" + reset()
        return msg

    def start(self, client_socket, player_name):
        print(color_green() + bold() + f"\nGAME STARTED NOW for client {player_name} !\n" + reset())
        time_now = time.time()
        self.__generate_equation()
        try:
            print(client_socket)
            # Sends problem to client.
            client_socket.sendall(self.get_begin_match_msg().encode())

            while TIME_OUT > time.time() - time_now:
                # Receiving answers from client.
                answer = client_socket.recv(BUFF_SIZE).decode()
                if not answer:
                    continue
                print(f"Answer received from {player_name}: " + answer)
                break

        except Exception as e:
            print_error(e)

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

        match operator:
            case "+":
                operand2 = random.randint(0, 9 - operand1)
                answer = operand1 + operand2
            case "-":
                operand2 = random.randint(0, operand1)
                answer = operand1 - operand2
            case "*":
                operand2 = random.randint(0, int(9 / operand1))
                answer = operand1 * operand2

        match operator_optional:
            case "+":
                operand_optional = random.randint(0, 9 - answer)
                answer += operand_optional
            case "-":
                operand_optional = random.randint(0, answer)
                answer -= operand_optional
            case "*":
                operand_optional = random.randint(0, int(9 / answer) if answer != 0 else int(9 / (answer + 1)))
                answer *= operand_optional

        optional = (" " + operator_optional + " " + operand_optional.__str__()) if operand_optional is not None else ""
        equation = operand1.__str__() + " " + operator + " " + operand2.__str__()
        equation = "(" + equation + ")" + optional if operand_optional is not None else equation

        self.__equation = equation
        self.__real_answer = answer
