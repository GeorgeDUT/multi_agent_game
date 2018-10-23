from war_1 import *
from red_brain import *
from blue_brain import *


def train_naive_brain(my_map,episode,red_win,blue_win):
    for step in range(1000):
        s=my_map.get_state()
        t_x,t_y=find_target(s)

        t_x_blue,t_y_blue=find_target_blue(s)

        red_action=[]
        blue_action=[]
        for i in range(my_map.red_num):
            a=goto_target(my_map.red_army[i].x,my_map.red_army[i].y,t_x,t_y)
            red_action.append(a)
        for i in range(my_map.blue_num):
            b=np.random.choice(['u','d','l','r','s'])
            # b=goto_target_blue(my_map.blue_army[i].x,my_map.blue_army[i].y,t_x_blue,t_y_blue)
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
    blue_win=[]
    red_win.append(0)
    blue_win.append(0)
    for episode in range(200):
        train_naive_brain(my_map,episode,red_win,blue_win)
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
    my_map = WarMap(30,30,28,28,True)
    if my_map.draw_pic:
        my_map.after(10,update)
        my_map.mainloop()
    else:
        update()