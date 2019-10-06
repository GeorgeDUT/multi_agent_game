"""
Using Reinforcement learning algorithm.
model is DQN_brain_new

"""

from DQN_brain_new import *
from function_brain import *
from war_4 import *
import matplotlib.pyplot as plt

MAP_H=10
MAP_W=10


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
    # s_map_change = np.zeros(MAP_W * MAP_H, )
    # for i in range(MAP_W):
    #     for j in range(MAP_H):
    #         s_map_change[i * MAP_W + j] = map[i, j]
    # return s_map_change
    s_map=np.zeros(my_map.red_num*2)
    for i in range(my_map.red_num):
        s_map[i*2]=my_map.red_army[i].x
        s_map[i*2+1]=my_map.red_army[i].y
    return s_map


def move_game(my_map):
    step=0.0
    s_map=change_map(my_map)

    while 1:
        step=step+1
        red_action=[]
        blue_action=[]

        """move action"""
        for i in range(my_map.blue_num):
            b=np.random.choice(['u','d','l','r','s'])
            # x,y=my_map.blue_army[i].x,my_map.blue_army[i].y
            # b=brain_blue(2,x,y,s.env_map)
            blue_action.append(b)

        red_num_action=Red_RL.choose_action(s_map)
        red_action=num_to_action(red_num_action,5,my_map.red_num)
        # for i in range(my_map.red_num):
        #     a=np.random.choice(['u','d','r','l','s'])
        #     red_action.append(a)


        #print(red_action,red_num_action)
        """move action"""

        my_map.move(red_action,blue_action)
        red,blue,red_kill,blue_kill,done=my_map.step()
        s_map_=change_map(my_map)

        if done:
            if red>blue:
                reward=(red-blue)*100
            else:
                reward=(red-blue)*100
        else:
            reward=0
        print(s_map,s_map_)
        Red_RL.store_transition(s_map,red_num_action,reward,s_map_)
        Red_RL.learn()
        s_map=s_map_


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
    plt_red_step=[]
    for episode in range(400):
        all=all+1
        r,step=move_game(my_map)
        sum_step=sum_step+step
        red_win=red_win+r
        print(red_win/all,sum_step/all)
        plt_red_win.append(red_win/all)
        plt_red_step.append(step)
    fig=plt.figure()
    plt.plot(plt_red_win)
    plt.show()



if __name__=="__main__":
    my_map=WarMap4(MAP_W,MAP_H,3,3,False,True)
    Red_RL=DeepQNetwork(
        n_actions=pow(5,my_map.red_num), n_features=my_map.red_num*2,
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