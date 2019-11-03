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

if __name__=="__main__":
    csvfile = open("protocol-8x8.csv", "w")
    writer = csv.writer(csvfile)
    writer.writerow(["timestamp","x1","y1","tx1","ty1","action"])
    direc=[[0,0],[0,0],[0,0],[0,0]]
    for id in range(4):
        for x1 in range(MAP_W):
            for y1 in range(MAP_H):
                for tx1 in range(MAP_W):
                    for ty1 in range(MAP_H):
                        target_x = max(0, tx1 + direc[id][0])
                        target_y = max(0, ty1 + direc[id][1])
                        target_x = min(MAP_W, target_x)
                        target_y = min(MAP_H, target_y)
                        direction_x = np.sign(x1 - target_x)
                        direction_y = np.sign(y1 - target_y)
                        '''
                        if(id==0):
                            if direction_x == -1 and direction_y == -1:
                                action = 'd'
                            elif direction_x == 1 and direction_y == 1:
                                action = 'u'
                            elif direction_x == 1 and direction_y == -1:
                                action = 'd'
                            elif direction_x == -1 and direction_y == 1:
                                action = 'r'
                            elif direction_x == 0 and direction_y == 1:
                                action = 'u'
                            elif direction_x == 0 and direction_y == -1:
                                action = 'd'
                            elif direction_x == 1 and direction_y == 0:
                                action = 'l'
                            elif direction_x == -1 and direction_y == 0:
                                action = 'r'
                            else:
                                action = 's'
                        elif(id==1):
                            if direction_x == -1 and direction_y == -1:
                                action = 'r'
                            elif direction_x == 1 and direction_y == 1:
                                action = 'l'
                            elif direction_x == 1 and direction_y == -1:
                                action = 'l'
                            elif direction_x == -1 and direction_y == 1:
                                action = 'u'
                            elif direction_x == 0 and direction_y == 1:
                                action = 'u'
                            elif direction_x == 0 and direction_y == -1:
                                action = 'd'
                            elif direction_x == 1 and direction_y == 0:
                                action = 'l'
                            elif direction_x == -1 and direction_y == 0:
                                action = 'r'
                            else:
                                action = 's'
                        elif(id==2):
                            if direction_x == -1 and direction_y == -1:
                                action = 'd'
                            elif direction_x == 1 and direction_y == 1:
                                action = 'u'
                            elif direction_x == 1 and direction_y == -1:
                                action = 'd'
                            elif direction_x == -1 and direction_y == 1:
                                action = 'u'
                            elif direction_x == 0 and direction_y == 1:
                                action = 'u'
                            elif direction_x == 0 and direction_y == -1:
                                action = 'd'
                            elif direction_x == 1 and direction_y == 0:
                                action = 'l'
                            elif direction_x == -1 and direction_y == 0:
                                action = 'r'
                            else:
                                action = 's'
                        elif(id==3):
                            if direction_x == -1 and direction_y == -1:
                                action = 'r'
                            elif direction_x == 1 and direction_y == 1:
                                action = 'l'
                            elif direction_x == 1 and direction_y == -1:
                                action = 'l'
                            elif direction_x == -1 and direction_y == 1:
                                action = 'r'
                            elif direction_x == 0 and direction_y == 1:
                                action = 'u'
                            elif direction_x == 0 and direction_y == -1:
                                action = 'd'
                            elif direction_x == 1 and direction_y == 0:
                                action = 'l'
                            elif direction_x == -1 and direction_y == 0:
                                action = 'r'
                            else:
                                action = 's'
                        dis_x = (x1 - tx1)
                        dis_y = (y1 - ty1)
                        '''

                        for timestamp in range(15):
                            if direction_x == -1 and direction_y == -1:
                                action = np.random.choice(['d', 'r', 'd', 'r', 'd', 'r','d', 'r', 'd', 'r', 'd', 'r',
                                                           'u', 'l'])
                            elif direction_x == 1 and direction_y == 1:
                                action = np.random.choice(['u', 'l', 'u', 'l', 'u', 'l', 'u', 'l', 'u', 'l', 'u', 'l',
                                                           'd', 'r'])
                            elif direction_x == 1 and direction_y == -1:
                                action = np.random.choice(['d', 'l', 'd', 'l', 'd', 'l', 'd', 'l', 'd', 'l', 'd', 'l',
                                                           'u', 'r'])
                            elif direction_x == -1 and direction_y == 1:
                                action = np.random.choice(['u', 'r', 'u', 'r', 'u', 'r', 'u', 'r', 'u', 'r', 'u', 'r',
                                                           'd', 'l'])

                            elif direction_x == 0 and direction_y == 1:
                                action = np.random.choice(['u', 'u', 'u', 'u', 'u', 'u', 'l', 'r'])
                            elif direction_x == 0 and direction_y == -1:
                                action = np.random.choice(['d', 'd', 'd', 'd', 'd', 'd', 'l', 'r'])
                            elif direction_x == 1 and direction_y == 0:
                                action = np.random.choice(['l', 'l', 'l', 'l', 'l', 'l', 'u', 'd'])
                            elif direction_x == -1 and direction_y == 0:
                                action = np.random.choice(['r', 'r', 'r', 'r', 'r', 'r', 'u', 'd'])
                            else:
                                action = np.random.choice(Action_Space)
                            dis_x=(x1-tx1)
                            dis_y=(y1-ty1)
                            '''
                            if (id==0):
                                if (dis_x==-1 and dis_y==-1):
                                    action='r'
                                elif (dis_x==0 and dis_y==-1):
                                    action='r'
                                elif (dis_x==1 and dis_y==-1):
                                    action='d'
                                elif (dis_x==1 and dis_y==0):
                                    action='d'
                                elif (dis_x==1 and dis_y==1):
                                    action='l'
                                elif (dis_x==0 and dis_y==1):
                                    action='l'
                                elif (dis_x==-1 and dis_y==1):
                                    action='u'
                                elif (dis_x==-1 and dis_y==0):
                                    action='u'
                            elif(id==1):
                                if (dis_x==-1 and dis_y==-1):
                                    action='l'
                                elif (dis_x==0 and dis_y==-1):
                                    action='l'
                                elif (dis_x==1 and dis_y==-1):
                                    action='u'
                                elif (dis_x==1 and dis_y==0):
                                    action='u'
                                elif (dis_x==1 and dis_y==1):
                                    action='r'
                                elif (dis_x==0 and dis_y==1):
                                    action='r'
                                elif (dis_x==-1 and dis_y==1):
                                    action='d'
                                elif (dis_x==-1 and dis_y==0):
                                    action='d'
                            elif (id==2):
                                if (dis_x==-1 and dis_y==-1):
                                    action='r'
                                elif (dis_x==0 and dis_y==-1):
                                    action='r'
                                elif (dis_x==1 and dis_y==-1):
                                    action='d'
                                elif (dis_x==1 and dis_y==0):
                                    action='d'
                                elif (dis_x==1 and dis_y==1):
                                    action='l'
                                elif (dis_x==0 and dis_y==1):
                                    action='l'
                                elif (dis_x==-1 and dis_y==1):
                                    action='u'
                                elif (dis_x==-1 and dis_y==0):
                                    action='u'
                            elif(id==3):
                                if (dis_x==-1 and dis_y==-1):
                                    action='l'
                                elif (dis_x==0 and dis_y==-1):
                                    action='s'
                                elif (dis_x==1 and dis_y==-1):
                                    action='u'
                                elif (dis_x==1 and dis_y==0):
                                    action='u'
                                elif (dis_x==1 and dis_y==1):
                                    action='r'
                                elif (dis_x==0 and dis_y==1):
                                    action='s'
                                elif (dis_x==-1 and dis_y==1):
                                    action='d'
                                elif (dis_x==-1 and dis_y==0):
                                    action='d'
                            '''
                            writer.writerow([timestamp, x1, y1, tx1, ty1, action])

