from war_1 import *
import pandas as pd


def value(s,x,y,team):
    if y>=len(s) or y<0 or x>=len(s[0]) or x<0:
        sum_dis,other_dis=9999,9999
    else:
        # compute x,y to other same team agent distance
        sum_dis = 0
        if team == 0:
            pass
        else:
            for i in range(len(s)):
                for j in range(len(s[0])):
                    if s[i][j] == team:
                        sum_dis = sum_dis + abs(y - i) + abs(x - j)
        # compute x,y to other other team agent distance
        other_dis=0
        if team == 0:
            pass
        else:
            for i in range(len(s)):
                for j in range(len(s[0])):
                    if s[i][j]+team==3:
                        other_dis = other_dis + abs(y - i) + abs(x - j)
    if team==1:
        all=-0.1*sum_dis-0.2*other_dis
    else:
        all=0*sum_dis-0*other_dis
    return all


def q_function(s,x,y,team):
    action_space=['u','d','l','r','s']
    move=[[0,-1],[0,1],[-1,0],[1,0],[0,0]]
    action=np.random.choice(action_space)
    action_value=[]
    for i in range(len(action_space)):
        v=value(s,x+move[i][0],y+move[i][1],team)
        action_value.append(v)
        if v==max(action_value):
            action=action_space[i]
        else:
            pass
    return action


def pseudo(my_map):
    while 1:
        red_action=[]
        blue_action=[]
        s=my_map.get_state()
        for i in range(my_map.red_num):
            x,y=my_map.red_army[i].x,my_map.red_army[i].y
            a=q_function(s.env_map,x,y,1)
            red_action.append(a)
        for i in range(my_map.blue_num):
            x,y=my_map.blue_army[i].x,my_map.blue_army[i].y
            b=q_function(s.env_map,x,y,2)
            b=np.random.choice(['u','d','l','r','s'])
            blue_action.append(b)

        my_map.move(red_action,blue_action)
        my_map.step()


def update():
    for episode in range(1000):
        pseudo(my_map)


if __name__ =="__main__":
    my_map=WarMap(30,30,28,28,True)
    if my_map.draw_pic:
        my_map.after(10,update)
        my_map.mainloop()
    else:
        update()
