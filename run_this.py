from war_1 import *
from red_brain import *
from blue_brain import *
from compiler.ast import flatten
import math


'''action_space: is |A|,agent_num: is number of red or blue agent'''


def num_to_action(num_action,action_space,agent_num):
    action_list=[]
    for i in range(agent_num):
        a=num_action%action_space
        num_action=num_action/action_space
        action_list.append(a)
    for i in range(len(action_list)):
        if action_list[i]== 0:
            action_list[i] = 'u'
        elif action_list[i]==1:
            action_list[i] = 'd'
        elif action_list[i]==2:
            action_list[i] = 'l'
        elif action_list[i]==3:
            action_list[i] = 'r'
        elif action_list[i]==4:
            action_list[i] = 's'
    return action_list


def train_dqn_brain(my_map,episode,red_win,blue_win):
    for step in range(1000):
        obs_red=my_map.get_state()
        action_red_num=RL_red.choose_action(obs_red.army_loc)
        action_red=num_to_action(action_red_num,5,my_map.red_num)
        '''blue action'''
        action_blue=[]
        for i in range(my_map.blue_num):
            b = np.random.choice(['u', 'd', 'l', 'r', 's'])
            # t_x_blue,t_y_blue=find_target_blue(s.env_map)
            # b=goto_target_blue(my_map.blue_army[i].x,my_map.blue_army[i].y,t_x_blue,t_y_blue)
            action_blue.append(b)
        '''blue action'''
        my_map.move(action_red,action_blue)
        red,blue,done=my_map.step()
        obs_red_=my_map.get_state()
        RL_red.store_transition(obs_red.army_loc,action_red_num,red,obs_red_.army_loc)
        if(step>200)and(step%5==0):
            RL_red.learn()

        obs_red=obs_red_

        if done:
            if red!=0:
                red_win[0]=red_win[0]+1
                print('red win:',red_win[0]*1.0/(episode+1))
            break


def train_naive_brain(my_map,episode,red_win,blue_win):
    for step in range(1000):
        s=my_map.get_state()
        t_x,t_y=find_target(s.env_map)

        t_x_blue,t_y_blue=find_target_blue(s.env_map)

        red_action=[]
        blue_action=[]
        for i in range(my_map.red_num):
            a=goto_target(my_map.red_army[i].x,my_map.red_army[i].y,t_x,t_y)
            a=np.random.choice(['u','d','l','r','s'])
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
            if red==0 and blue==0:
                print('draw')
            break


def update():
    all=0
    red_win=[]
    blue_win=[]
    red_win.append(0)
    blue_win.append(0)
    for episode in range(5000):
        train_naive_brain(my_map,episode,red_win,blue_win)
        # train_dqn_brain(my_map,episode,red_win,blue_win)
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
    num_to_action(76,5,3)
    my_map = WarMap(4,6,2,2,False)
    action_space=math.pow(5,my_map.red_num)
    RL_red=DQN(action_space,(my_map.red_num+my_map.blue_num)*4,learning_rate=0.01,reward_decay=0.9,e_greedy=0.9,replace_target_iter=200,memory_size=2000,)
    if my_map.draw_pic:
        my_map.after(10,update)
        my_map.mainloop()
    else:
        update()