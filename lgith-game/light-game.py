"""
Using Reinforcement learning algorithm.
model is DQN_brain

"""

from war_4 import *
# import matplotlib.pyplot as plt

MAP_H=50
MAP_W=50

Action_Space=['u','d','l','r','s']

def cmt_light(my_map):
    pass

def move_game(my_map):
    step=0.0
    s_map_list=[]
    s_map_next_list=[]

    while 1:
        print(my_map.env_map)
        step=step+1
        red_action=[]
        blue_action=[]
        """move action"""
        for i in range(my_map.blue_num):
            b=np.random.choice(['u','d','l','r','s'])
            blue_action.append(b)
        for i in range(my_map.red_num):
            a=np.random.choice(['u','d','l','r','s'])
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