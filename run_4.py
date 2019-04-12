"""
this file is feature function
"""
from war_4 import *
import numpy as np
import tensorflow as tf
# print(tf.__version__)
# a=tf.constant([1,2,3],shape=[1,3],name='a')
# b=tf.constant([1,2,3],shape=[3,1],name='b')
# c=tf.matmul(a,b)
# sess=tf.Session(config=tf.ConfigProto(log_device_placement=True))
# print(sess.run(c))


# [-0.1,-1,-90],[10,1,0]
#
weight_r=[-0.1,-1,-90]
weight_b=[-1,1,0]


MAP_H=40
MAP_W=40

dis_of_red=[]
dis_of_blue=[]


# transform map to list of red and blue
def map_to_list(s_loc):
    del dis_of_red[:]
    del dis_of_blue[:]
    for i in range(len(s_loc[0])):
        if s_loc[0][i][2]==1:
            a=[]
            a.append(s_loc[0][i][0])
            a.append(s_loc[0][i][1])
            dis_of_red.append(a)
    for i in range(len(s_loc[1])):
        if s_loc[1][i][2]==1:
            a = []
            a.append(s_loc[1][i][0])
            a.append(s_loc[1][i][1])
            dis_of_blue.append(a)


def dis(x1,y1,x2,y2):
    return abs(x1-x2)+abs(y1-y2)


'''
def dis(x1,y1,x2,y2):
    d_1=abs(x1-x2)+abs(y1-y2)
    d_2=(MAP_W-abs(x1-x2))+abs(MAP_H-abs(y1-y2))
    d=min(d_1,d_2)
    d=d_1-d_2
    return d
'''


# x is w; y is h
# compute the distance of each other in our group
def function_1(num,s_map,s_loc):
    sum_distance=0
    if num==1:
        for i in range(len(dis_of_red)):
            for j in range(len(dis_of_red)):
                sum_distance=sum_distance+dis(dis_of_red[i][0],dis_of_red[i][1],
                             dis_of_red[j][0],dis_of_red[j][1])
    else:
        for i in range(len(dis_of_blue)):
            for j in range(len(dis_of_blue)):
                sum_distance=sum_distance+dis(dis_of_blue[i][0],dis_of_blue[i][1],
                             dis_of_blue[j][0],dis_of_blue[j][1])
    return sum_distance


# compute the distance of each pair (our agent, enemy agent)
def function_2(num,s_map,s_loc):
    sum_distance = 0
    for i in range(len(dis_of_blue)):
        for j in range(len(dis_of_red)):
            sum_distance = sum_distance + dis(dis_of_blue[i][0], dis_of_blue[i][1],
                                              dis_of_red[j][0], dis_of_red[j][1])
    return sum_distance


# compute the min distance pair (our agent, enemy agent)
def function_3(num,s_map,s_loc):
    min_dis=len(s_map)+len(s_map[0])
    for i in range(len(dis_of_blue)):
        for j in range(len(dis_of_red)):
            pair_dis=dis(dis_of_blue[i][0],dis_of_blue[i][1],dis_of_red[j][0],dis_of_red[j][1])
            min_dis=min(min_dis,pair_dis)
    return min_dis


def sum_function_r(num,s_map,s_loc):
    map_to_list(s_loc)
    value = weight_r[0]*function_1(num,s_map,s_loc)+weight_r[1]*function_2(num,s_map,s_loc)+weight_r[2]*function_3(num,s_map,s_loc)
    return value


def sum_function_b(num,s_map,s_loc):
    map_to_list(s_loc)
    value = weight_b[0]*function_1(num,s_map,s_loc)+weight_b[1]*function_2(num,s_map,s_loc)+weight_b[2]*function_3(num,s_map,s_loc)
    return value


def want_move_r(num,x,y,action,s_map,s_loc):
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
    for i in range(len(s_loc[0])):
        if x==s_loc[0][i][0] and y==s_loc[0][i][1] and s_loc[0][i][2]==1:
            s_loc[0][i][0]=x_new
            s_loc[0][i][1]=y_new
            break
    sum_distance=sum_function_r(num,s_map,s_loc)
    s_map[y][x]=num
    s_map[y_new][x_new]=0
    for i in range(len(s_loc[0])):
        if x_new==s_loc[0][i][0] and y_new==s_loc[0][i][1] and s_loc[0][i][2]==1:
            s_loc[0][i][0]=x
            s_loc[0][i][1]=y
            break
    return sum_distance


def want_move_b(num,x,y,action,s_map,s_loc):
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

    for i in range(len(s_loc[1])):
        if x==s_loc[1][i][0] and y==s_loc[1][i][1] and s_loc[1][i][2]==1:
            s_loc[1][i][0]=x_new
            s_loc[1][i][1]=y_new
            break

    sum_distance=sum_function_b(num,s_map,s_loc)
    s_map[y][x]=num
    s_map[y_new][x_new]=0
    for i in range(len(s_loc[1])):
        if x_new==s_loc[1][i][0] and y_new==s_loc[1][i][1] and s_loc[1][i][2]==1:
            s_loc[1][i][0]=x
            s_loc[1][i][1]=y
            break
    return sum_distance


def brain_red(num,x,y,s_map,s_loc):
    action_space=['u','d','l','r','s']
    random.shuffle(action_space)
    action_reward=[]
    for action in action_space:
        r=want_move_r(num,x,y,action,s_map,s_loc)
        action_reward.append(r)
    choose=action_reward.index(max(action_reward))
    return action_space[choose]


def brain_blue(num,x,y,s_map,s_loc):
    action_space=['u','d','l','r','s']
    random.shuffle(action_space)
    action_reward=[]
    for action in action_space:
        r=want_move_b(num,x,y,action,s_map,s_loc)
        action_reward.append(r)
    choose=action_reward.index(max(action_reward))
    return action_space[choose]


def move_game(my_map):
    while 1:
        # time.sleep(0.002)
        red_action=[]
        blue_action=[]
        s=my_map.get_state()
        s_loc=[]
        s_loc.append(s.red_loc)
        s_loc.append(s.blue_loc)
        s_map=s.env_map

        for i in range(my_map.red_num):
            x,y=my_map.red_army[i].x,my_map.red_army[i].y
            a=brain_red(1,x,y,s_map,s_loc)
            # a='r'
            red_action.append(a)
        for i in range(my_map.blue_num):
            x,y=my_map.blue_army[i].x,my_map.blue_army[i].y
            #b=np.random.choice(['u','d','r','l','s'])
            b=brain_blue(2,x,y,s_map,s_loc)
            blue_action.append(b)

        my_map.move(red_action,blue_action)
        red,blue,done=my_map.step()
        if done:
            print ('end')


def update():
    for episode in range(100):
        move_game(my_map)


if __name__=="__main__":
    my_map=WarMap4(MAP_W,MAP_H,15,10,True,True)
    if my_map.draw_pic:
        my_map.after(10,update)
        my_map.mainloop()
    else:
        update()
