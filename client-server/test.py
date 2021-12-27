import msvcrt
import threading


from lib import KeyListen

if __name__ == '__main__':
    #match = Match.Match()
    #match.start()
   # print(f"Problem: {match.get_math_problem()}, Answer: {match.get_real_answer()}")



    c = msvcrt.getch()
    print(f"you pressed: {c.decode()}")
    # print(f"{c}")
    