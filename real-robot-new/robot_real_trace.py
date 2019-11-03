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
[0, 0, 1, 0, 2, 0, 3, 0, 1, 7],
[0, 1, 1, 1, 1, 0, 3, 1, 1, 7],
[0, 2, 0, 1, 1, 1, 2, 1, 0, 7],
[0, 3, 0, 1, 2, 1, 2, 0, 1, 7],
[1, 3, 1, 1, 2, 1, 2, 0, 1, 7],
[2, 3, 0, 1, 2, 2, 1, 0, 1, 7],
[1, 3, 0, 1, 3, 2, 1, 1, 1, 7],
[1, 4, 0, 2, 3, 3, 1, 2, 1, 7],
[0, 4, 1, 2, 3, 4, 1, 3, 1, 7],
[0, 5, 1, 3, 3, 5, 1, 4, 2, 7],
[0, 5, 1, 3, 2, 5, 1, 5, 2, 7],
[0, 5, 2, 3, 2, 6, 1, 6, 2, 7],
[1, 5, 3, 3, 3, 6, 1, 6, 1, 7],
[0, 5, 4, 3, 3, 7, 1, 6, 1, 7],
[1, 5, 4, 4, 2, 7, 0, 6, 1, 7],
[1, 6, 3, 4, 2, 7, 0, 7, 1, 7],
]


def choose_action(step,team,id):
    x_next=Trace[step][((team-1)*4+id)*2]
    y_next=Trace[step][((team-1)*4+id)*2+1]
    return x_next,y_next


def move_game(my_map):
    step=0
    trace=[]
    while 1:
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
                      my_map.red_army[3].x, my_map.red_army[3].y,
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

    my_map=WarMap4(MAP_W,MAP_H,4,1,True,False)

    if my_map.draw_pic:
        my_map.after(10,update)
        my_map.mainloop()
    else:
        update()