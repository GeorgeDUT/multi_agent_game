"""
Using Reinforcement learning algorithm.
model is DQN_brain

"""

from war_4 import *
# import matplotlib.pyplot as plt

MAP_H=50
MAP_W=50

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


def move_game(my_map):
    step=0.0
    s_map_list=[]
    s_map_next_list=[]
    while 1:
        step=step+1
        red_action=[]
        blue_action=[]
        """move action"""
        for i in range(my_map.blue_num):
            b=np.random.choice(Action_Space)
            blue_action.append(b)
        for i in range(my_map.red_num):
            a=cmt_light(my_map,my_map.red_army[i].x,my_map.red_army[i].y)
            red_action.append(a)
        """move action"""
        my_map.move(red_action,blue_action)
        my_map.step()


def update():
    red_win,all,sum_step=0.0,0.0,0.0
    plt_red_win=[]
    plt_red_step=[]
    for episode in range(500):
        all=all+1
        r,step=move_game(my_map)
        sum_step=sum_step+step
        red_win=red_win+r
        # print(red_win/all,sum_step/all)
        print(r,step)
        plt_red_win.append(red_win/all)
        plt_red_step.append(step)


if __name__=="__main__":
    my_map=WarMap4(MAP_W,MAP_H,20,20,True,False)

    if my_map.draw_pic:
        my_map.after(10,update)
        my_map.mainloop()
    else:
        update()