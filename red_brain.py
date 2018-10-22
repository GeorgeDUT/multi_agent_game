import random


def find_target(s):
    for i in range(len(s)):
        for j in range(len(s[0])):
            if s[i][j]==2:
                x,y=j,i
                break
    return x,y


def goto_target(x,y,t_x,t_y):
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
    return action