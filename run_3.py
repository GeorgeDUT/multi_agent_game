"""
this file is feature function
"""
from war_3 import *
import numpy as np


weight=[-0.1,-0]
bais=10


def dis(x1,y1,x2,y2):
    return abs(x1-x2)+abs(y1-y2)


# x is w; y is h
# compute the distance of each other in red group
def function_1(num,s_map):
    dis_of_red=[]
    for i in range(len(s_map)):
        for j in range(len(s_map[0])):
            a=[]
            if s_map[i][j]==num:
                a.append(j)
                a.append(i)
                dis_of_red.append(a)
    sum_distance=0
    for i in range(len(dis_of_red)):
        for j in range(len(dis_of_red)):
            sum_distance=sum_distance+dis(dis_of_red[i][0],dis_of_red[i][1],
                             dis_of_red[j][0],dis_of_red[j][1])
    return sum_distance


def function_2(num,s_map):
    dis_of_red = []
    dis_of_blue=[]
    for i in range(len(s_map)):
        for j in range(len(s_map[0])):
            a = []
            b=[]
            if s_map[i][j] != num and s_map[i][j]!=0:
                a.append(j)
                a.append(i)
                dis_of_red.append(a)
            if s_map[i][j]==num:
                b.append(j)
                b.append(i)
                dis_of_blue.append(b)
    sum_distance = 0
    for i in range(len(dis_of_blue)):
        for j in range(len(dis_of_red)):
            sum_distance = sum_distance + dis(dis_of_blue[i][0], dis_of_blue[i][1],
                                              dis_of_red[j][0], dis_of_red[j][1])
    return sum_distance


def sum_function(num,s_map):
    return weight[0]*function_1(num,s_map)+weight[1]*function_2(num,s_map)


def want_move(num,x,y,action,s_map):
    if action =='u':
        x_new=x
        y_new=max(0,y-1)
    elif action=='d':
        x_new=x
        y_new=min(y+1,len(s_map)-1)
    elif action=='l':
        x_new=max(0,x-1)
        y_new=y
    elif action=='r':
        x_new=min(x+1,len(s_map[0])-1)
        y_new=y
    else:
        x_new=x
        y_new=y
    s_map[y][x]=0
    s_map[y_new][x_new]=num
    sum_distance=sum_function(num,s_map)
    s_map[y][x]=num
    s_map[y_new][x_new]=0
    return sum_distance


def brain_red(num,x,y,s_map):
    action_space=['u','d','l','r','s']
    random.shuffle(action_space)
    action_reward=[]
    for action in action_space:
        r=want_move(num,x,y,action,s_map)
        action_reward.append(r)
    choose=action_reward.index(max(action_reward))
    return action_space[choose]


def move_game(my_map):
    while 1:
        # time.sleep(0.002)
        red_action=[]
        blue_action=[]
        s=my_map.get_state()
        s_map=s.env_map
        for i in range(my_map.red_num):
            x,y=my_map.red_army[i].x,my_map.red_army[i].y
            a=brain_red(1,x,y,s_map)
            red_action.append(a)
        for i in range(my_map.blue_num):
            x,y=my_map.blue_army[i].x,my_map.blue_army[i].y
            b=np.random.choice(['u','d','r','l','s'])
            blue_action.append(b)

        my_map.move(red_action,blue_action)
        red,blue,done=my_map.step()
        if done:
            print ('end')


def update():
    for episode in range(100):
        move_game(my_map)


if __name__=="__main__":
    my_map=WarMap3(20,20,10,5,True)
    if my_map.draw_pic:
        my_map.after(10,update)
        my_map.mainloop()
    else:
        update()
