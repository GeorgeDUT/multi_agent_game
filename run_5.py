"""
Using Reinforcement learning algorithm.

"""

from DQN_brain_new import *
from war_4 import *
import matplotlib.pyplot as plt

MAP_H=6
MAP_W=6


def num_to_action(action_id,action_num,agent_num):
    action_space=['u','d','l','r','s']
    b=[]
    while True:
        s = action_id // action_num
        y = action_id % action_num
        b.append(action_space[y])
        if s == 0:
            break
        action_id = s
    l=len(b)
    for i in range(l,agent_num):
        b.append('u')
    return b


def change_map(map):
    s_map_change = np.zeros(MAP_W * MAP_H, )
    for i in range(MAP_W):
        for j in range(MAP_H):
            s_map_change[i * MAP_W + j] = map[i, j]
    return s_map_change


def move_game(my_map):
    step=0.0
    s=my_map.get_state()
    s_map=s.env_map
    s_map=change_map(s_map)

    while 1:
        step=step+1
        red_action=[]
        blue_action=[]

        """move action"""
        for i in range(my_map.blue_num):
            b=np.random.choice(['u','d','r','l','s'])
            blue_action.append(b)

        red_num_action=Red_RL.choose_action(s_map)
        red_action=num_to_action(red_num_action,5,my_map.red_num)
        # for i in range(my_map.red_num):
        #     a=np.random.choice(['u','d','r','l','s'])
        #     red_action.append(a)


        #print(red_action,red_num_action)
        """move action"""

        my_map.move(red_action,blue_action)
        red,blue,done=my_map.step()
        s_=my_map.get_state()
        s_map_=s_.env_map
        s_map_=change_map(s_map_)

        if done:
            if red>blue:
                reward=100
            else:
                reward=-100
        else:
            reward=0
        Red_RL.store_transition(s_map,red_num_action,reward,s_map_)

        if done:
            print ('end',red,blue,step)
            if red>blue:
                return 1,step
            elif red==blue:
                return 0.5,step
            else:
                return 0,step


def update():
    red_win,all,sum_step=0.0,0.0,0.0
    plt_red_win=[]
    for episode in range(200):
        all=all+1
        r,step=move_game(my_map)
        sum_step=sum_step+step
        red_win=red_win+r
        print(red_win/all,sum_step/all)
        plt_red_win.append(red_win/all)
    fig=plt.figure()
    plt.plot(plt_red_win)
    plt.show()



if __name__=="__main__":
    my_map=WarMap4(MAP_W,MAP_H,4,4,False,True)
    Red_RL=DeepQNetwork(
        n_actions=pow(5,my_map.red_num), n_features=MAP_H*MAP_W,
        learning_rate=0.01,
        reward_decay=0.9,
        e_greedy=0.9,
        replace_target_iter=200,
        memory_size=2000,
    )
    # Blue_RL=DeepQNetwork(
    #     n_actions=pow(my_map.blue_num,5), n_features=MAP_W*MAP_H,
    #     learning_rate=0.01,
    #     reward_decay=0.9,
    #     e_greedy=0.9,
    #     replace_target_iter=200,
    #     memory_size=2000,
    # )
    if my_map.draw_pic:
        my_map.after(10,update)
        my_map.mainloop()
    else:
        update()