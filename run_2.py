from war_1 import *
import pandas as pd


def q_function(s,x,y):
    action_space=['u','d','l','r','s']
    action=np.random.choice(action_space)
    action_value=[]
    for i in range(len(action_space)):
        action_value.append(1)
    return action


def pseudo(my_map):
    while 1:
        red_action=[]
        blue_action=[]
        s=my_map.get_state()
        for i in range(my_map.red_num):
            x,y=my_map.red_army[i].x,my_map.red_army[i].y
            a=q_function(s.env_map,x,y)
            red_action.append(a)
        for i in range(my_map.blue_num):
            x,y=my_map.blue_army[i].x,my_map.blue_army[i].y
            b=q_function(s.env_map,x,y)
            blue_action.append(b)

        my_map.move(red_action,blue_action)
        my_map.step()


def update():
    for episode in range(1000):
        pseudo(my_map)


if __name__ =="__main__":
    my_map=WarMap(25,25,13,13,True)
    if my_map.draw_pic:
        my_map.after(10,update)
        my_map.mainloop()
    else:
        update()
