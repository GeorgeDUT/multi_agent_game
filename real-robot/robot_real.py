"""
Using Reinforcement learning algorithm.
model is DQN_brain

"""

from war_real import *
# import matplotlib.pyplot as plt
import csv
import pandas as pd

MAP_H=8
MAP_W=8
Action_Space=['u','d','l','r','s']
Blue_action_list_1=['u','d','l','l','l','r','r']
data=pd.read_csv("protocol-8x8.csv")


def choose_action(i,x,y,tx,ty):
    a=data[(data['timestamp']==i)&(data['x1']==x) & (data['y1']==y)
           & (data['tx1']==tx) &(data['ty1']==ty)]['action']
    a=a.tolist()
    return a[0]


def move_game(my_map):
    step=0
    trace=[]
    while 1:
        red_action=[]
        blue_action=[]
        if step==0:
            trace.append([my_map.red_army[0].x, my_map.red_army[0].y,
                                        my_map.red_army[1].x, my_map.red_army[1].y,
                                        my_map.red_army[2].x, my_map.red_army[2].y,
                                        my_map.red_army[3].x, my_map.red_army[3].y,
                                        my_map.blue_army[0].x, my_map.blue_army[0].y]
                                       )

        """move action"""
        for i in range(my_map.blue_num):
            b=np.random.choice(Action_Space)
            # b=Blue_action_list_1[int(step%len(Blue_action_list_1))]
            # b = np.random.choice(['u', 'd', 'l','l', 'r', 'r', 'r','r','r','r'])
            # b = np.random.choice(['u', 'd', 'l', 'l', 'l', 'l', 'l'])
            blue_action.append(b)
        for i in range(my_map.red_num):
            a=choose_action(random.randint(0,14),my_map.red_army[i].x,my_map.red_army[i].y,
                            my_map.blue_army[0].x,my_map.blue_army[0].y)
            red_action.append(a)
        """move action"""

        my_map.move(red_action,blue_action)

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