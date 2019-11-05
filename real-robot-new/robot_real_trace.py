"""
move order give x,y flash map

"""

"""
Using Reinforcement learning algorithm.
model is DQN_brain

"""

from war_bace_trace import *
# import matplotlib.pyplot as plt
import csv
import pandas as pd

MAP_H=8
MAP_W=8
Action_Space=['u','d','l','r','s']
Blue_action_list_1=['u','d','l','l','l','r','r']
Trace=[
[0, 0, 1, 0, 2, 0, 1, 7],
[0, 1, 1, 1, 2, 0, 2, 7],
[0, 1, 1, 2, 2, 1, 3, 7],
[0, 1, 2, 2, 2, 1, 4, 7],
[0, 2, 2, 3, 2, 2, 5, 7],
[0, 3, 3, 3, 2, 2, 6, 7],
[0, 4, 2, 3, 2, 1, 7, 7],
[0, 3, 2, 4, 2, 2, 7, 7],
[0, 4, 3, 4, 2, 3, 7, 7],
[1, 4, 3, 3, 2, 4, 7, 7],
[1, 5, 3, 4, 2, 5, 7, 7],
[1, 4, 3, 5, 2, 6, 7, 6],
[2, 4, 4, 5, 3, 6, 7, 5],
[3, 4, 5, 5, 4, 6, 7, 5],
[3, 5, 6, 5, 5, 6, 7, 5],
[4, 5, 6, 5, 5, 7, 7, 5],
[5, 5, 6, 5, 5, 7, 7, 5],
[6, 5, 6, 4, 5, 6, 7, 5],
[6, 5, 7, 4, 5, 5, 7, 5],
[6, 4, 7, 4, 5, 4, 6, 5],
[6, 5, 7, 4, 5, 4, 5, 5],
[6, 5, 7, 5, 5, 4, 5, 6],
[6, 5, 7, 6, 5, 5, 6, 6],
[6, 5, 7, 6, 5, 6, 6, 6],
[6, 5, 7, 6, 5, 6, 6, 6],
[6, 5, 7, 6, 5, 5, 6, 6],
[6, 5, 7, 6, 5, 6, 6, 6],
[6, 5, 7, 5, 5, 6, 6, 6],
[5, 5, 6, 5, 6, 6, 7, 6],
[5, 6, 6, 4, 6, 6, 7, 6],
[6, 6, 6, 5, 6, 7, 7, 6],
[6, 6, 6, 5, 7, 7, 7, 6],
[6, 6, 6, 5, 7, 7, 7, 6],
[6, 6, 7, 5, 6, 7, 7, 6],
[6, 6, 7, 5, 7, 7, 7, 6],


# [0, 0, 1, 0, 2, 0, 3, 0, 1, 7],
# [0, 1, 1, 1, 1, 0, 3, 0, 2, 7],
# [0, 1, 1, 2, 2, 0, 3, 1, 2, 7],
# [1, 1, 1, 3, 3, 0, 2, 1, 2, 7],
# [1, 1, 1, 4, 2, 0, 2, 2, 2, 7],
# [1, 2, 2, 4, 1, 0, 2, 3, 2, 7],
# [2, 2, 1, 4, 2, 0, 2, 3, 3, 7],
# [3, 2, 2, 4, 3, 0, 3, 3, 3, 7],
# [3, 3, 2, 4, 4, 0, 3, 4, 3, 7],
# [3, 3, 3, 4, 4, 1, 3, 5, 4, 7],
# [3, 3, 4, 4, 4, 2, 4, 5, 4, 7],
# [3, 4, 4, 4, 4, 3, 4, 6, 4, 7],
# [3, 5, 5, 4, 5, 3, 4, 6, 4, 7],
# [2, 5, 4, 4, 5, 4, 5, 6, 4, 7],
# [2, 6, 4, 5, 5, 4, 6, 6, 4, 7],
# [2, 7, 4, 6, 5, 5, 6, 7, 5, 7],
# [3, 7, 4, 7, 5, 5, 5, 7, 5, 6],
# [3, 7, 4, 7, 5, 5, 5, 7, 5, 6],
# [4, 7, 4, 6, 5, 5, 5, 7, 5, 6],
# [4, 7, 4, 6, 5, 5, 5, 7, 5, 6],
# [4, 7, 4, 6, 5, 5, 5, 7, 5, 6],
# [4, 7, 4, 6, 5, 5, 6, 7, 5, 6],
# [4, 7, 4, 6, 6, 5, 6, 6, 5, 6],
# [3, 7, 4, 6, 6, 4, 6, 6, 5, 5],
# [3, 6, 5, 6, 6, 5, 6, 6, 5, 5],
# [3, 5, 5, 6, 6, 5, 6, 6, 5, 5],
# [3, 4, 5, 5, 6, 5, 7, 6, 5, 4],
# [3, 4, 4, 5, 6, 4, 6, 6, 4, 4],
# [3, 4, 4, 5, 6, 5, 5, 6, 4, 4],
# [3, 4, 4, 5, 6, 4, 5, 5, 4, 4],
# [3, 5, 4, 5, 5, 4, 5, 5, 4, 4],
# [3, 4, 4, 5, 5, 4, 5, 5, 4, 4],
# [3, 4, 4, 5, 4, 4, 5, 5, 4, 3],
# [3, 4, 4, 5, 4, 4, 5, 5, 4, 3],
# [3, 4, 4, 5, 4, 4, 6, 5, 3, 3],
# [2, 4, 3, 5, 4, 4, 6, 4, 4, 3],
# [3, 4, 4, 5, 4, 4, 6, 3, 4, 3],
# [2, 4, 4, 4, 4, 3, 5, 3, 3, 3],
# [3, 4, 4, 5, 4, 3, 5, 3, 3, 3],
# [4, 4, 3, 5, 4, 3, 5, 3, 3, 3],
# [3, 4, 3, 5, 4, 3, 5, 2, 3, 2],
# [3, 3, 2, 5, 4, 4, 4, 2, 3, 2],
# [3, 3, 2, 4, 5, 4, 4, 2, 2, 2],
# [2, 3, 2, 4, 4, 4, 3, 2, 1, 2],
# [1, 3, 2, 3, 4, 3, 3, 1, 0, 2],
# [1, 2, 2, 2, 4, 2, 2, 1, 0, 2],
# [0, 2, 1, 2, 3, 2, 2, 2, 0, 1],
# [0, 2, 1, 1, 3, 1, 2, 1, 0, 0],
# [0, 1, 1, 1, 3, 0, 2, 1, 0, 0],
# [0, 1, 1, 0, 3, 0, 2, 1, 0, 0]


# [0, 0, 1, 0, 2, 0, 3, 0, 1, 7],
# [0, 0, 1, 1, 1, 0, 3, 0, 1, 7],
# [0, 1, 1, 2, 1, 1, 2, 0, 1, 7],
# [0, 1, 1, 3, 1, 1, 1, 0, 1, 6],
# [0, 1, 1, 4, 1, 1, 1, 0, 1, 6],
# [0, 1, 1, 5, 1, 1, 0, 0, 1, 6],
# [0, 2, 1, 5, 1, 2, 1, 0, 2, 6],
# [0, 3, 2, 5, 2, 2, 1, 1, 3, 6],
# [1, 3, 3, 5, 3, 2, 1, 2, 3, 6],
# [1, 4, 3, 5, 3, 3, 1, 3, 3, 6],
# [0, 4, 4, 5, 3, 4, 1, 3, 3, 6],
# [0, 5, 3, 5, 3, 4, 2, 3, 3, 7],
# [0, 6, 3, 6, 3, 5, 2, 4, 4, 7],
# [0, 7, 4, 6, 3, 6, 2, 5, 4, 7],
# [1, 7, 4, 7, 4, 6, 2, 6, 5, 7],
# [2, 7, 5, 7, 4, 6, 2, 5, 6, 7],
# [3, 7, 6, 7, 4, 7, 3, 5, 6, 6],
# [4, 7, 6, 7, 4, 6, 4, 5, 6, 6],
# [5, 7, 6, 7, 5, 6, 5, 5, 6, 6],
# [5, 7, 6, 6, 5, 6, 5, 5, 7, 6],
# [6, 7, 6, 5, 6, 6, 5, 5, 7, 5],
# [6, 7, 6, 4, 7, 6, 5, 5, 7, 5],
# [5, 7, 6, 3, 6, 6, 6, 5, 7, 4],
# [4, 7, 6, 2, 6, 7, 6, 4, 7, 4],
# [5, 7, 6, 3, 7, 7, 7, 4, 7, 5],
# [5, 6, 6, 4, 7, 6, 7, 4, 6, 5],
# [5, 5, 6, 4, 6, 6, 7, 5, 6, 5],


]


def choose_action(step,team,id):
    x_next=Trace[step][((team-1)*3+id)*2]
    y_next=Trace[step][((team-1)*3+id)*2+1]
    return x_next,y_next


def move_game(my_map):
    step=0
    trace=[]
    while 1:
        num = input()
        x=[]
        y=[]
        x_b=[]
        y_b=[]
        if step==0:
            trace.append([my_map.red_army[0].x, my_map.red_army[0].y,
                                        my_map.red_army[1].x, my_map.red_army[1].y,
                                        my_map.red_army[2].x, my_map.red_army[2].y,
                                        # my_map.red_army[3].x, my_map.red_army[3].y,
                                        my_map.blue_army[0].x, my_map.blue_army[0].y]
                                       )

        """move action"""

        for i in range(my_map.blue_num):
            action_x,action_y=choose_action(step,2,i)
            x_b.append(action_x)
            y_b.append(action_y)
            # b=Blue_action_list_1[int(step%len(Blue_action_list_1))]
            # b = np.random.choice(['u', 'd', 'l','l', 'r', 'r', 'r','r','r','r'])
            # b = np.random.choice(['u', 'd', 'l', 'l', 'l', 'l', 'l'])
        for i in range(my_map.red_num):
            action_x, action_y = choose_action(step, 1, i)
            x.append(action_x)
            y.append(action_y)
        """move action"""
        print (x,y,x_b,y_b)
        my_map.move(x,y,x_b,y_b)

        trace.append([my_map.red_army[0].x, my_map.red_army[0].y,
                      my_map.red_army[1].x, my_map.red_army[1].y,
                      my_map.red_army[2].x, my_map.red_army[2].y,
                      # my_map.red_army[3].x, my_map.red_army[3].y,
                      my_map.blue_army[0].x, my_map.blue_army[0].y]
                     )

        # trace.append([my_map.red_army[0].x, my_map.red_army[0].y,
        #               my_map.red_army[1].x, my_map.red_army[1].y,
        #               my_map.red_army[2].x, my_map.red_army[2].y,
        #               my_map.red_army[3].x, my_map.red_army[3].y,
        #               my_map.blue_army[0].x, my_map.blue_army[0].y]
        #              )
        # print(trace[step])

        reward_red, reward_blue, red_killed, blue_killed, done=my_map.step()

        if done:
            for i in range(len(trace)):
                print(trace[i])

            print('done',done)
            break
        time.sleep(0)
        step = step + 1
    return step


def update():
    for episode in range(500):
        step=move_game(my_map)
        print('step',step)

if __name__=="__main__":

    my_map=WarMap4(MAP_W,MAP_H,3,1,True,False)

    if my_map.draw_pic:
        my_map.after(10,update)
        my_map.mainloop()
    else:
        update()