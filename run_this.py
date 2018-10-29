# from war_2 import *
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


def train_dqn_brain(my_map,episode,red_win,blue_win,r_red):
    r_red[0]=0
    for step in range(99999):
        if episode>200:
            # time.sleep(0.1)
            pass
        obs_red=my_map.get_state()
        action_red_num=RL_red.choose_action(obs_red.army_loc)
        action_red=num_to_action(action_red_num,5,my_map.red_num)
        '''blue action'''
        action_blue=[]
        for i in range(my_map.blue_num):
            b = np.random.choice(['d', 'r', 'r', 'r', 'd'])
            # t_x_blue,t_y_blue=find_target_blue(s.env_map)
            # b=goto_target_blue(my_map.blue_army[i].x,my_map.blue_army[i].y,t_x_blue,t_y_blue)
            action_blue.append(b)
        '''blue action'''
        my_map.move(action_red,action_blue)
        red,blue,done=my_map.step()
        obs_red_=my_map.get_state()
        RL_red.store_transition(obs_red.army_loc,action_red_num,red,obs_red_.army_loc)
        r_red[0]=r_red[0]+red
        if(episode>5)and(step%5==0):
            RL_red.learn()

        obs_red=obs_red_

        if done:
            if red!=0:
                red_win[0]=red_win[0]+1
                print('red win:',red_win[0]*1.0/(episode+1),'step',step)
            break
    print('reward',r_red[0])


def train_naive_brain(my_map,episode,red_win,blue_win):
    for step in range(1000):
        s=my_map.get_state()
        t_x,t_y=find_target(s.env_map)

        t_x_blue,t_y_blue=find_target_blue(s.env_map)

        red_action=[]
        blue_action=[]
        for i in range(my_map.red_num):
            # a=goto_target_blue(my_map.red_army[i].x,my_map.red_army[i].y,t_x,t_y,s.env_map)
            a=np.random.choice(['u','d','l','r','s'])
            red_action.append(a)
        for i in range(my_map.blue_num):
            b=np.random.choice(['l','l','d','d','l'])
            # b=goto_target_blue(my_map.blue_army[i].x,my_map.blue_army[i].y,t_x_blue,t_y_blue,s.env_map)
            blue_action.append(b)

        my_map.move(red_action,blue_action)
        red, blue, done = my_map.step()
        if done:
            if red != 0:
                red_win[0]=red_win[0]+1
                print('red win:',red_win[0]*1.0/(episode+1),'step',step)
            if red == 0 and blue == 0:
                print('draw')
            if blue!=0:
                blue_win[0]=blue_win[0]+1
                print('blue win:',blue_win[0]*1.0/(episode+1),'step',step)
            break


def train_high_brain(my_map,episode,red_win,blue_win,r_red):
    r_red[0] = 0
    for step in range(99999):
        if episode > 200:
            # time.sleep(0.1)
            pass
        obs_red = my_map.get_state()
        while 1:
            action_red_num = RL_red.choose_action(obs_red.army_loc)
            if my_map.blue_army[action_red_num].life=='live':
                break
        '''red action'''
        action_red=[]
        for i in range(my_map.red_num):
            t_x_red,t_y_red=my_map.blue_army[action_red_num].x,my_map.blue_army[action_red_num].y
            a=goto_target(my_map.red_army[i].x,my_map.red_army[i].y,t_x_red,t_y_red,obs_red.env_map)
            action_red.append(a)
        '''red action'''

        '''blue action'''
        if 0<=step%80<=40:
            action_blue = []
            for i in range(my_map.blue_num):
                b = np.random.choice(['d', 'd', 'd', 'd', 'd'])
                # t_x_blue,t_y_blue=find_target_blue(s.env_map)
                # b=goto_target_blue(my_map.blue_army[i].x,my_map.blue_army[i].y,t_x_blue,t_y_blue,obs_red.env_map)
                action_blue.append(b)
        else:
            action_blue = []
            for i in range(my_map.blue_num):
                b = np.random.choice(['u', 'u', 'u', 'u', 'u'])
                # t_x_blue,t_y_blue=find_target_blue(s.env_map)
                # b=goto_target_blue(my_map.blue_army[i].x,my_map.blue_army[i].y,t_x_blue,t_y_blue,obs_red.env_map)
                action_blue.append(b)
        '''blue action'''
        my_map.move(action_red, action_blue)
        red, blue, done = my_map.step()
        obs_red_ = my_map.get_state()
        RL_red.store_transition(obs_red.army_loc, action_red_num, red, obs_red_.army_loc)
        r_red[0] = r_red[0] + red
        if (episode > 5) and (step % 5 == 0):
            RL_red.learn()

        obs_red = obs_red_

        if done:
            if red != 0:
                red_win[0] = red_win[0] + 1
                print('red win:', red_win[0] * 1.0 / (episode + 1), 'step', step)
            break


def update():
    all=0
    red_win=[]
    blue_win=[]
    r_red=[]
    red_win.append(0)
    blue_win.append(0)
    r_red.append(0)
    for episode in range(1000):
        #train_naive_brain(my_map,episode,red_win,blue_win)
        train_high_brain(my_map,episode,red_win,blue_win,r_red)
        # train_dqn_brain(my_map,episode,red_win,blue_win,r_red)
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
    my_map = WarMap(20,20,15,15,False)
    # action_space=math.pow(5,my_map.red_num)
    action_space=my_map.blue_num
    RL_red=DQN(action_space,(my_map.red_num+my_map.blue_num)*4,learning_rate=0.01,reward_decay=0.9,e_greedy=0.9,replace_target_iter=200,memory_size=2000,)
    if my_map.draw_pic:
        my_map.after(10,update)
        my_map.mainloop()
    else:
        update()