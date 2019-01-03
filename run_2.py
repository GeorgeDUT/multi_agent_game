"""
this function is just for war_3 game
usr force, every pair of agents have force like gravity.

"""
from war_3 import *
import pandas as pd
import math


def cmpt_f_r(s,x,y):

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

    red_force=[0.,0.]
    blue_force=[0.,0.]
    # cmpt red sum force
    F=0.0
    for i in range(s.red_num):
        # random find a target
        # i=random.randint(0,s.red_num-1)
        # i=(i+s.red_num/2)%s.red_num
        end_x,end_y=int(s.red_loc[i][0]),int(s.red_loc[i][1])
        if s.env_map[end_y][end_x]==1:
            f_x, f_y = force(x, y, end_x, end_y)
            '''
            # red force rule 1: sum force is all force
            red_force[0]+=f_x
            red_force[1]+=f_y
            '''

            # red force rule 2: max force is all force
            F=max(pow(f_x,2)+pow(f_y,2),F)
            if F==pow(f_x,2)+pow(f_y,2):
                red_force[0],red_force[1]=f_x,f_y

        else:
            pass
    # cmpt blue sum force
    F=0.0
    for i in range(s.blue_num):
        i=random.randint(0,s.blue_num-1)
        end_x,end_y=int(s.blue_loc[i][0]),int(s.blue_loc[i][1])
        if s.env_map[end_y][end_x]==2:
            f_x,f_y=force(x,y,end_x,end_y)

            # blue force rule 1:外力乘以距离的四次方。
            blue_force[0] += f_x*pow((pow(x - end_x, 2) + pow(y - end_y, 2)),1)
            blue_force[1] += f_y*pow((pow(x - end_x, 2) + pow(y - end_y, 2)),1)

            '''
            # blue force rule 2: max force is his all force
            F = max(pow(f_x, 2) + pow(f_y, 2), F)
            if F == pow(f_x, 2) + pow(f_y, 2):
                blue_force[0], blue_force[1] = f_x, f_y
            '''
            '''
            # blue force rule 3:sum force
            blue_force[0] += f_x
            blue_force[1] += f_y
            '''

        else:
            pass
    return red_force,blue_force


def brain_r(s,x,y,team,id):

    def softmax(x):
        return np.exp(x) / np.sum(np.exp(x), axis=0)

    action_space = ['u', 'd', 'l', 'r', 's']
    action = np.random.choice(action_space)
    red_f,blue_f=cmpt_f_r(s,x,y)
    r_sum_f,b_sum_f=[0.,0.],[0.,0.]
    # his is blue all sum force-1
    # r_sum_f[0]=red_f[0]+(blue_f[0]*pow(0.1,-1))
    # r_sum_f[1] = red_f[1] + (blue_f[1]*pow(0.1,-1))
    r_sum_f[0] = red_f[0]* 0 + (blue_f[0] * pow(0.1, -1))
    r_sum_f[1] = red_f[1] *0+ (blue_f[1]*pow(0.1,-1))

    b_sum_f[0] = red_f[0] + (blue_f[0] * pow(0.1, 6))
    b_sum_f[1] = red_f[1] + (blue_f[1] * pow(0.1, 6))

    # this is blue all sum force-2
    '''
    red_f[0] = red_f[0] + (blue_f[0] * pow(0.1, 2.5))
    red_f[1] = red_f[1] + (blue_f[1] * pow(0.1, 2.5))
    '''

    # choose direction
    pi_r = softmax([abs(r_sum_f[0]), abs(r_sum_f[1])])
    pi_b = softmax([abs(b_sum_f[0]), abs(b_sum_f[1])])
    if team==1:
        if r_sum_f[0]>0 and r_sum_f[1]>=0:
            if np.random.rand()<pi_r[0]:
                action='r'
            else:
                action='d'
        elif r_sum_f[0]<=0<r_sum_f[1]:
            if np.random.rand() < pi_r[0]:
                action = 'l'
            else:
                action = 'd'
        elif r_sum_f[0]<0 and r_sum_f[1]<=0:
            if np.random.rand() < pi_r[0]:
                action = 'l'
            else:
                action = 'u'
        elif r_sum_f[0]>=0>r_sum_f[1]:
            if np.random.rand() < pi_r[0]:
                action = 'r'
            else:
                action = 'u'
        '''
        elif r_sum_f[0]==0 and r_sum_f[1]>0:
            action='d'
        elif r_sum_f[0]==0 and r_sum_f[1]<0:
            action = 'u'
        elif r_sum_f[0]>0 and r_sum_f[1]==0:
            action = 'r'
        elif r_sum_f[0]<0 and r_sum_f[1]==0:
            action = 'l'
        '''
    elif team==2:
        if b_sum_f[0] > 0 and b_sum_f[1] >= 0:
            if np.random.rand() < pi_b[0]:
                action = 'r'
            else:
                action = 'd'
        elif b_sum_f[0] <= 0 < b_sum_f[1]:
            if np.random.rand() < pi_b[0]:
                action = 'l'
            else:
                action = 'd'
        elif b_sum_f[0] < 0 and b_sum_f[1] <= 0:
            if np.random.rand() < pi_b[0]:
                action = 'l'
            else:
                action = 'u'
        elif b_sum_f[0] >= 0 > b_sum_f[1]:
            if np.random.rand() < pi_b[0]:
                action = 'r'
            else:
                action = 'u'
        '''
        elif b_sum_f[0]==0 and b_sum_f[1]>0:
            action='d'
        elif b_sum_f[0]==0 and b_sum_f[1]<0:
            action = 'u'
        elif b_sum_f[0]>0 and b_sum_f[1]==0:
            action = 'r'
        elif b_sum_f[0]<0 and b_sum_f[1]==0:
            action = 'l'
        '''
    return action


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

    red_force=[0.,0.]
    blue_force=[0.,0.]
    # cmpt red sum force
    F=0.0
    for i in range(s.red_num):
        # random find a target
        # i=random.randint(0,s.red_num-1)
        # i=(i+s.red_num/2)%s.red_num
        end_x,end_y=int(s.red_loc[i][0]),int(s.red_loc[i][1])
        if s.env_map[end_y][end_x]==1:
            f_x, f_y = force(x, y, end_x, end_y)
            '''
            # red force rule 1: sum force is all force
            red_force[0]+=f_x
            red_force[1]+=f_y
            '''

            # red force rule 2: max force is all force
            F=max(pow(f_x,2)+pow(f_y,2),F)
            if F==pow(f_x,2)+pow(f_y,2):
                red_force[0],red_force[1]=f_x,f_y

        else:
            pass
    # cmpt blue sum force
    F=0.0
    for i in range(s.blue_num):
        i=random.randint(0,s.blue_num-1)
        end_x,end_y=int(s.blue_loc[i][0]),int(s.blue_loc[i][1])
        if s.env_map[end_y][end_x]==2:
            f_x,f_y=force(x,y,end_x,end_y)

            # blue force rule 1:外力乘以距离的四次方。
            blue_force[0] += f_x*pow((pow(x - end_x, 2) + pow(y - end_y, 2)),1)
            blue_force[1] += f_y*pow((pow(x - end_x, 2) + pow(y - end_y, 2)),1)

            '''
            # blue force rule 2: max force is his all force
            F = max(pow(f_x, 2) + pow(f_y, 2), F)
            if F == pow(f_x, 2) + pow(f_y, 2):
                blue_force[0], blue_force[1] = f_x, f_y
            '''
            '''
            # blue force rule 3:sum force
            blue_force[0] += f_x
            blue_force[1] += f_y
            '''

        else:
            pass
    return red_force,blue_force


def brain(s,x,y,team,id):

    def softmax(x):
        return np.exp(x) / np.sum(np.exp(x), axis=0)

    action_space = ['u', 'd', 'l', 'r', 's']
    action = np.random.choice(action_space)
    red_f,blue_f=cmpt_f(s,x,y)
    r_sum_f,b_sum_f=[0.,0.],[0.,0.]
    # his is blue all sum force-1
    # r_sum_f[0]=red_f[0]+(blue_f[0]*pow(0.1,-1))
    # r_sum_f[1] = red_f[1] + (blue_f[1]*pow(0.1,-1))
    r_sum_f[0] = red_f[0] + (blue_f[0] * pow(0.1, 1))
    r_sum_f[1] = red_f[1] + (blue_f[1]*pow(0.1,1))

    b_sum_f[0] = red_f[0] + (blue_f[0] * pow(0.1, 6))
    b_sum_f[1] = red_f[1] + (blue_f[1] * pow(0.1, 6))

    # this is blue all sum force-2
    '''
    red_f[0] = red_f[0] + (blue_f[0] * pow(0.1, 2.5))
    red_f[1] = red_f[1] + (blue_f[1] * pow(0.1, 2.5))
    '''

    # choose direction
    pi_r = softmax([abs(r_sum_f[0]), abs(r_sum_f[1])])
    pi_b = softmax([abs(b_sum_f[0]), abs(b_sum_f[1])])
    if team==1:
        if r_sum_f[0]>0 and r_sum_f[1]>=0:
            if np.random.rand()<pi_r[0]:
                action='r'
            else:
                action='d'
        elif r_sum_f[0]<=0<r_sum_f[1]:
            if np.random.rand() < pi_r[0]:
                action = 'l'
            else:
                action = 'd'
        elif r_sum_f[0]<0 and r_sum_f[1]<=0:
            if np.random.rand() < pi_r[0]:
                action = 'l'
            else:
                action = 'u'
        elif r_sum_f[0]>=0>r_sum_f[1]:
            if np.random.rand() < pi_r[0]:
                action = 'r'
            else:
                action = 'u'
        '''
        elif r_sum_f[0]==0 and r_sum_f[1]>0:
            action='d'
        elif r_sum_f[0]==0 and r_sum_f[1]<0:
            action = 'u'
        elif r_sum_f[0]>0 and r_sum_f[1]==0:
            action = 'r'
        elif r_sum_f[0]<0 and r_sum_f[1]==0:
            action = 'l'
        '''
    elif team==2:
        if b_sum_f[0] > 0 and b_sum_f[1] >= 0:
            if np.random.rand() < pi_b[0]:
                action = 'r'
            else:
                action = 'd'
        elif b_sum_f[0] <= 0 < b_sum_f[1]:
            if np.random.rand() < pi_b[0]:
                action = 'l'
            else:
                action = 'd'
        elif b_sum_f[0] < 0 and b_sum_f[1] <= 0:
            if np.random.rand() < pi_b[0]:
                action = 'l'
            else:
                action = 'u'
        elif b_sum_f[0] >= 0 > b_sum_f[1]:
            if np.random.rand() < pi_b[0]:
                action = 'r'
            else:
                action = 'u'
        '''
        elif b_sum_f[0]==0 and b_sum_f[1]>0:
            action='d'
        elif b_sum_f[0]==0 and b_sum_f[1]<0:
            action = 'u'
        elif b_sum_f[0]>0 and b_sum_f[1]==0:
            action = 'r'
        elif b_sum_f[0]<0 and b_sum_f[1]==0:
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
            a=brain_r(s,x,y,1,i)
            # a=np.random.choice(['s','u','d','l','r'])
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
