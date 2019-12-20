"""
Using Reinforcement learning algorithm.
model is DQN_brain

"""

from war_real import *
# import matplotlib.pyplot as plt
import csv
import pandas as pd

MAP_H=6
MAP_W=6


Action_Space=['u','d','l','r','s']


def cmt_light(my_map,x,y):
    dis_to_blue=[]
    for i in range(my_map.blue_num):
        if my_map.blue_army[i].life!='live':
            dis=my_map.map_w*my_map.map_h
        else:
            dis=abs(x-my_map.blue_army[i].x)+\
                abs(y-my_map.blue_army[i].y)
        dis_to_blue.append(dis)
    blue_target=dis_to_blue.index(min(dis_to_blue))
    print(blue_target)
    x_b=my_map.blue_army[blue_target].x
    y_b=my_map.blue_army[blue_target].y
    direction_x=np.sign(x-x_b)
    direction_y=np.sign(y-y_b)
    if direction_x==-1 and direction_y==-1:
        action=np.random.choice(['d','r','d','r','d','r','u','l'])
    elif direction_x==1 and direction_y==1:
        action=np.random.choice(['u','l','u','l','u','l','d','r'])
    elif direction_x==1 and direction_y==-1:
        action=np.random.choice(['d','l','d','l','d','l','u','r'])
    elif direction_x==-1 and direction_y==1:
        action=np.random.choice(['u','r','u','r','u','r','d','l'])

    elif direction_x==0 and direction_y==1:
        action=np.random.choice(['u','u','u','u','u','u','l','r'])
    elif direction_x==0 and direction_y==-1:
        action=np.random.choice(['d','d','d','d','d','d','l','r'])
    elif direction_x==1 and direction_y==0:
        action=np.random.choice(['l','l','l','l','l','l','u','d'])
    elif direction_x==-1 and direction_y==0:
        action=np.random.choice(['r','r','r','r','r','r','u','d'])
    else:
        action=np.random.choice(Action_Space)
    return action

def cmt_light_blue(my_map,x,y):
    dis_to_red=[]
    for i in range(my_map.red_num):
        if my_map.red_army[i].life!='live':
            dis=my_map.map_w*my_map.map_h
        else:
            dis=abs(x-my_map.red_army[i].x)+\
                abs(y-my_map.red_army[i].y)
        dis_to_red.append(dis)
    red_target=dis_to_red.index(min(dis_to_red))
    print(red_target)
    x_b=my_map.red_army[red_target].x
    y_b=my_map.red_army[red_target].y
    direction_x=np.sign(x-x_b)
    direction_y=np.sign(y-y_b)
    if direction_x==-1 and direction_y==-1:
        action=np.random.choice(['d','r','d','r','d','r','u','l'])
    elif direction_x==1 and direction_y==1:
        action=np.random.choice(['u','l','u','l','u','l','d','r'])
    elif direction_x==1 and direction_y==-1:
        action=np.random.choice(['d','l','d','l','d','l','u','r'])
    elif direction_x==-1 and direction_y==1:
        action=np.random.choice(['u','r','u','r','u','r','d','l'])

    elif direction_x==0 and direction_y==1:
        action=np.random.choice(['u','u','u','u','u','u','l','r'])
    elif direction_x==0 and direction_y==-1:
        action=np.random.choice(['d','d','d','d','d','d','l','r'])
    elif direction_x==1 and direction_y==0:
        action=np.random.choice(['l','l','l','l','l','l','u','d'])
    elif direction_x==-1 and direction_y==0:
        action=np.random.choice(['r','r','r','r','r','r','u','d'])
    else:
        action=np.random.choice(Action_Space)
    return action


def move_game(my_map):
    step=0
    trace=[]
    while 1:
        line = sys.stdin.readline()
        red_action=[]
        blue_action=[]
        if step==0:
            trace.append([my_map.red_army[0].x, my_map.red_army[0].y,
                                        my_map.red_army[1].x, my_map.red_army[1].y,
                                        my_map.red_army[2].x, my_map.red_army[2].y,
                                        my_map.red_army[3].x, my_map.red_army[3].y,
                                        my_map.blue_army[0].x, my_map.blue_army[0].y,
                                        my_map.blue_army[1].x, my_map.blue_army[1].y,
                                        my_map.blue_army[2].x, my_map.blue_army[2].y,
                                        my_map.blue_army[3].x, my_map.blue_army[3].y]
                         )
            print(trace[-1])

        """move action"""
        for i in range(my_map.blue_num):
            b=np.random.choice(Action_Space)
            # b = np.random.choice(['u', 'u', 'u','u', 'u'])
            blue_action.append(b)
        for i in range(my_map.red_num):
            a=cmt_light(my_map,my_map.red_army[i].x,my_map.red_army[i].y)
            red_action.append(a)
        """move action"""
        my_map.move(red_action,blue_action)

        loc_x_r=[]
        loc_y_r=[]
        for agent_num in range (my_map.red_num):
            if my_map.red_army[agent_num].life=='live':
                loc_x_r.append(my_map.red_army[agent_num].x)
                loc_y_r.append(my_map.red_army[agent_num].y)
            else:
                loc_x_r.append(-1)
                loc_y_r.append(-1)

        loc_x_b = []
        loc_y_b = []
        for agent_num in range(my_map.blue_num):
            if my_map.blue_army[agent_num].life == 'live':
                loc_x_b.append(my_map.blue_army[agent_num].x)
                loc_y_b.append(my_map.blue_army[agent_num].y)
            else:
                loc_x_b.append(-1)
                loc_y_b.append(-1)

        trace.append([loc_x_r[0],loc_y_r[0],
                      loc_x_r[1], loc_y_r[1],
                      loc_x_r[2], loc_y_r[2],
                      loc_x_r[3], loc_y_r[3],
                      loc_x_b[0], loc_y_b[0],
                      loc_x_b[1], loc_y_b[1],
                      loc_x_b[2], loc_y_b[2],
                      loc_x_b[3], loc_y_b[3],
                      ]
                     )
        print(trace[-1])
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

    my_map=WarMap4(MAP_W,MAP_H,4,4,True,False)

    if my_map.draw_pic:
        my_map.after(10,update)
        my_map.mainloop()
    else:
        update()