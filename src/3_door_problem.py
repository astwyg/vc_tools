# result:
# change win rate:0.667088
# no change win rate:0.33338

import random


def game_env(flag):
    door = random.choice(["001","010","100"])
    choice = random.randint(0, 2)

    # show goat
    choices = [x for x in range(3)]
    if door[choice] == "1":
        choices.remove(choice)
        cnt = random.choice(choices)
        door = door[:cnt] + "x" + door[cnt+1:]
    else:
        for cnt in range(3):
            if cnt != choice and door[cnt]=="0":
                door = door[:cnt] + "x" + door[cnt+1:]

    if flag == "change":
        if door[choice] == "0":
            return "win"
        else:
            return "lose"
    else:
        if door[choice] == "1":
            return "win"
        else:
            return "lose"


if __name__ == '__main__':
    random.seed(12306)
    win_cnt = 0
    times = 1000000
    for _ in range(times):
        if game_env("change") == "win":
            win_cnt += 1
    print("change win rate:{}".format(win_cnt/times))

    win_cnt = 0
    for _ in range(times):
        if game_env("no_change") == "win":
            win_cnt += 1
    print("no change win rate:{}".format(win_cnt/times))


