"""
this function is just for war_3 game
usr force, every pair of agents have force like gravity.

"""
from war_3 import *
import pandas as pd
import math


def cmpt_f(s,x,y):

    def force(start_x, start_y, end_x, end_y):
        distance_2 = (pow(start_x - end_x, 2) + pow(start_y - end_y, 2))
        if distance_2 == 0:
            return 0, 0
        f = 1.0 / distance_2
        x, y = end_x - start_x, end_y - start_y
        # f^2=(kx)^2+(ky)^2
        f_x = f * x / (pow(x * x + y * y, 0.5))
        f_y = f * y / (pow(x * x + y * y, 0.5))
        return f_x, f_y

    red_force=[0,0]
    blue_force=[0,0]
    F=0.0
    for i in range(s.red_num):
        # random find a target
        # i=random.randint(0,s.red_num-1)
        # i=(i+s.red_num/2)%s.red_num
        end_x,end_y=int(s.red_loc[i][0]),int(s.red_loc[i][1])
        if s.env_map[end_y][end_x]==1:
            f_x,f_y=force(x,y,end_x,end_y)

            red_force[0]+=f_x
            red_force[1]+=f_y
            break
            '''
            F=max(pow(f_x,2)+pow(f_y,2),F)
            if F==pow(f_x,2)+pow(f_y,2):
                red_force[0],red_force[1]=f_x,f_y
            '''
        else:
            pass
    F=0.0
    for i in range(s.blue_num):
        i=random.randint(0,s.blue_num-1)
        end_x,end_y=int(s.blue_loc[i][0]),int(s.blue_loc[i][1])
        if s.env_map[end_y][end_x]==2:
            f_x,f_y=force(x,y,end_x,end_y)
            blue_force[0] += f_x*pow((pow(x - end_x, 2) + pow(y - end_y, 2)),2)
            blue_force[1] += f_y*pow((pow(x - end_x, 2) + pow(y - end_y, 2)),2)
            '''
            F = max(pow(f_x, 2) + pow(f_y, 2), F)
            if F == pow(f_x, 2) + pow(f_y, 2):
                blue_force[0], blue_force[1] = f_x, f_y
            '''
            break
        else:
            pass
    return red_force,blue_force


def brain(s,x,y,team,id):

    def softmax(x):
        return np.exp(x) / np.sum(np.exp(x), axis=0)

    action_space = ['u', 'd', 'l', 'r', 's']
    action = np.random.choice(action_space)
    red_f,blue_f=cmpt_f(s,x,y)
    red_f[0]=red_f[0]+(blue_f[0]*pow(0.1,5))
    red_f[1] = red_f[1] + (blue_f[1]*pow(0.1,5))

    # choose direction
    pi = softmax([abs(red_f[0]), abs(red_f[1])])
    if red_f[0]>0 and red_f[1]>=0:
        if np.random.rand()<pi[0]:
            action='r'
        else:
            action='d'
    elif red_f[0]<=0<red_f[1]:
        if np.random.rand() < pi[0]:
            action = 'l'
        else:
            action = 'd'
    elif red_f[0]<0 and red_f[1]<=0:
        if np.random.rand() < pi[0]:
            action = 'l'
        else:
            action = 'u'
    elif red_f[0]>=0>red_f[1]:
        if np.random.rand() < pi[0]:
            action = 'r'
        else:
            action = 'u'
    '''
    elif red_f[0]==0 and red_f[1]>0:
        action='d'
    elif red_f[0]==0 and red_f[1]<0:
        action = 'u'
    elif red_f[0]>0 and red_f[1]==0:
        action = 'r'
    elif red_f[0]<0 and red_f[1]==0:
        action = 'l'
    '''

    return action


def pseudo(my_map):
    while 1:
        time.sleep(0)
        red_action=[]
        blue_action=[]
        s=my_map.get_state()
        for i in range(my_map.red_num):
            x,y=my_map.red_army[i].x,my_map.red_army[i].y
            a=brain(s,x,y,1,i)
            a=np.random.choice(['u','d','l','r','s'])
            red_action.append(a)
        for i in range(my_map.blue_num):
            x,y=my_map.blue_army[i].x,my_map.blue_army[i].y
            b=brain(s,x,y,2,i)
            blue_action.append(b)
        my_map.move(red_action,blue_action)
        red,blue,done=my_map.step()
        if done:
            print('end')


def update():
    for episode in range(1000):
        pseudo(my_map)


if __name__ =="__main__":
    my_map=WarMap3(80,60,50,50,True)
    if my_map.draw_pic:
        my_map.after(10,update)
        my_map.mainloop()
    else:
        update()
