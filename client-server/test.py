import msvcrt
import threading
import time

import lib.KeyListen

from lib import KeyListen

if __name__ == '__main__':
    # match = Match.Match()
    # match.start()
    # print(f"Problem: {match.get_math_problem()}, Answer: {match.get_real_answer()}")

    num = 0
    done = False
    end_time = time.time() + 5

    while end_time > time.time():

        if msvcrt.kbhit():
            print(
                "you pressed", msvcrt.getch(), "so now i will quit")
            break

    print("ENDDDDDD")


