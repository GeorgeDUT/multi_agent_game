"""
Using Reinforcement learning algorithm.
model is DQN_brain

"""

from draw_value_map import *
# import matplotlib.pyplot as plt

MAP_H=100
MAP_W=100

Action_Space=['s','s','s','s','s']


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
        action=np.random.choice(Action_Space)
    elif direction_x==1 and direction_y==1:
        action=np.random.choice(Action_Space)
    elif direction_x==1 and direction_y==-1:
        action=np.random.choice(Action_Space)
    elif direction_x==-1 and direction_y==1:
        action=np.random.choice(['u','r','u','r','u','r','d','l'])

    elif direction_x==0 and direction_y==1:
        action=np.random.choice(Action_Space)
    elif direction_x==0 and direction_y==-1:
        action=np.random.choice(Action_Space)
    elif direction_x==1 and direction_y==0:
        action=np.random.choice(Action_Space)
    elif direction_x==-1 and direction_y==0:
        action=np.random.choice(Action_Space)
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
            # b=np.random.choice(['u','d','l','l','l','l','l'])
            # b = np.random.choice(['u', 'd', 'l','l', 'r', 'r', 'r','r','r','r'])
            # b = np.random.choice(['u', 'd', 'l', 'l', 'l', 'l', 'l'])
            blue_action.append(b)
        for i in range(my_map.red_num):
            a=cmt_light(my_map,my_map.red_army[i].x,my_map.red_army[i].y)
            red_action.append(a)
        """move action"""
        my_map.move(red_action,blue_action)
        my_map.step()
        time.sleep(20)


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
    my_map=WarMap4(MAP_W,MAP_H,100,150,True,False)

    if my_map.draw_pic:
        my_map.after(10,update)
        my_map.mainloop()
    else:
        update()