import random
import tensorflow as tf
import numpy as np


def find_target_blue(s):
    for i in range(len(s)):
        for j in range(len(s[0])):
            if s[i][j]==1:
                x,y=j,i
                return x, y
                # break
    return x,y


def goto_target_blue(x,y,t_x,t_y,env_map):
    other_dis=[]
    averge=0.0
    for i in range(len(env_map)):
        for j in range(len(env_map[0])):
            if env_map[i][j]==2:
                dis=abs(t_x-j)+abs(t_y-i)
                other_dis.append(dis)
    for i in range(len(other_dis)):
        averge=averge+other_dis[i]*1.0/len(other_dis)

    if (abs(t_x-x)+abs(t_y-y))<averge*0.9:
        action = 's'
    else:
        '''find short path start bfs'''
        dis_map=np.zeros(shape=(len(env_map),len(env_map[0])))
        for i in range(len(dis_map)):
            for j in range(len(dis_map[0])):
                dis_map[i][j]=9999
        dir=[[1,0],[-1,0],[0,1],[0,-1]]
        dis_map[t_y][t_x]=0
        que=[]
        que.append([t_x,t_y])
        # flag=1,find a path, else no
        flag = 0
        while len(que):
            front=que[0]
            del(que[0])
            if front[0]==x and front[1]==y:
                flag=1
                break
            for i in range(4):
                n_x=front[0]+dir[i][0]
                n_y=front[1]+dir[i][1]
                if 0<=n_x<len(env_map[0]) and 0<=n_y<len(env_map) and dis_map[n_y][n_x]==9999 and env_map[n_y][n_x]==0:
                    dis_map[n_y][n_x]=dis_map[front[1]][front[0]]+1
                    que.append([n_x,n_y])
                if n_x==x and n_y==y:
                    dis_map[n_y][n_x] = dis_map[front[1]][front[0]] + 1
                    que.append([n_x, n_y])
        '''find short path end'''
        if flag==1:
            short_dir = []
            for i in range(4):
                to_x = x + dir[i][0]
                to_y = y + dir[i][1]
                if 0 <= to_x < len(env_map[0]) and 0 <= to_y < len(env_map):
                    short_dir.append(dis_map[to_y][to_x])
                else:
                    short_dir.append(9999)
            if short_dir.index(min(short_dir)) == 0:
                action = 'r'
            elif short_dir.index(min(short_dir)) == 1:
                action = 'l'
            elif short_dir.index(min(short_dir)) == 2:
                action = 'd'
            elif short_dir.index(min(short_dir)) == 3:
                action = 'u'
        else:
            if x > t_x and y >= t_y:
                if random.random() > 0.8:
                    action = 'l'
                else:
                    action = 'u'
            elif x <= t_x and y > t_y:
                if random.random() > 0.2:
                    action = 'r'
                else:
                    action = 'u'
            elif x < t_x and y <= t_y:
                if random.random() > 0.8:
                    action = 'r'
                else:
                    action = 'd'
            elif x >= t_x and y < t_y:
                if random.random() > 0.2:
                    action = 'l'
                else:
                    action = 'd'
            else:
                action = 's'

    '''
    if x>t_x and y>=t_y:
        if random.random()>0.8:
            action='l'
        else:
            action='u'
    elif x<=t_x and y>t_y:
        if random.random()>0.2:
            action='r'
        else:
            action='u'
    elif x < t_x and y <= t_y:
        if random.random()> 0.8:
            action = 'r'
        else:
            action = 'd'
    elif x>=t_x and y<t_y:
        if random.random() > 0.2:
            action = 'l'
        else:
            action = 'd'
    else:
        action='s'
    '''
    return action