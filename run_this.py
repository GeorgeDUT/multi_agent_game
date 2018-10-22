from war_1 import *
from red_brain import *
import tensorflow as tf


def train_naive_brain(my_map,episode,red_win):
    for step in range(1000):
        s=my_map.get_state()
        t_x,t_y=find_target(s)
        red_action=[]
        blue_action=[]
        for i in range(my_map.red_num):
            a=goto_target(my_map.red_army[i].x,my_map.red_army[i].y,t_x,t_y)
            red_action.append(a)
        for i in range(my_map.blue_num):
            b=np.random.choice(['u','d','l','r','s'])
            blue_action.append(b)

        my_map.move(red_action,blue_action)
        red, blue, done = my_map.step()
        if done:
            if red!=0:
                red_win[0]=red_win[0]+1
                print('red win:',red_win[0]*1.0/(episode+1))
            break



def update():
    all=0
    red_win=[]
    red_win.append(0)
    for episode in range(300):
        train_naive_brain(my_map,episode,red_win)
    '''

        my_map.move(a, b)
        red, blue,done =my_map.step()
        if done:
            all=all+1
            if red!=0:
                red_win=red_win+1
            print('red win:',red_win*1.0/all)
    '''
        

if __name__ == "__main__":
    my_map = WarMap(13,6,12,10,True)
    if my_map.draw_pic:
        my_map.after(10,update)
        my_map.mainloop()
    else:
        update()