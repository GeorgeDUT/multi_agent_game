"""
war_s come from war_4
different:
    rule red must surround blue, blue can be removed.

"""

from __future__ import division
import time
import numpy as np
import math
import sys
import random
import numpy as np
if sys.version_info.major == 2:
    from Tkinter import *
    import Tkinter as tk
else:
    from tkinter import *
    import tkinter as tk


MAP_W = 5
MAP_H = 5
UNIT_PIX = 10
R_ARMY_NUM = 5
B_ARMY_NUM = 5
Block=10

print('this is war_3: Ant world war')


class Army(object):
    def __init__(self,x=0,y=0,id=0,team=0,life='live'):
        self.x=x
        self.y=y
        self.id=id
        self.team=team
        self.life=life
        self.win_p=1
        self.power=1
        self.blood=100


class OutInfo(object):
    def __init__(self, h, w, red_num, blue_num):
        self.env_map=np.zeros(shape=(h,w))
        self.red_num=red_num
        self.blue_num=blue_num
        '''loc [x,y,live or dead]'''
        self.red_loc=np.zeros(shape=(red_num,3))
        self.blue_loc=np.zeros(shape=(blue_num,3))
        # self.army_loc=np.zeros((red_num+blue_num)*4)
        # self.feature_stat=np.zeros(int(math.pow(2,blue_num)))


class WarMap4(tk.Tk, object):
    def __init__(self, w=MAP_W, h=MAP_H, red=R_ARMY_NUM, blue=B_ARMY_NUM, draw_pic=False,global_switch=False):
        self.draw_pic = draw_pic
        self.global_switch=global_switch
        self.map_w = w
        self.map_h = h
        self.red_num = red
        self.blue_num = blue
        # env_map = 0, space; =1,red_army; =2, blue_army; =10, block=3
        self.env_map = np.zeros(shape=(self.map_h, self.map_w))
        self.red_army = []
        self.blue_army = []
        self.red_army_draw=[]
        self.blue_army_draw=[]
        self.block_draw=[]
        # agent [id] is live agent.
        self.red_live_id=[]
        self.blue_live_id=[]
        # generation block
        self.block = np.zeros((Block, 2))
        for i in range(Block):
            self.block[i, 0] = random.randint(1, self.map_w - 1)
            self.block[i, 1] = random.randint(1, self.map_h - 2)

        self._init_map()


        if draw_pic:
            super(WarMap4,self).__init__()
            self.title('Ant world war')
            self.geometry('{0}x{1}'.format(self.map_w*UNIT_PIX, self.map_h*UNIT_PIX))
            self._display_window()
        else:
            pass

    def _init_map(self):
        self.red_army=[]
        self.blue_army=[]
        self.red_live_id=[]
        self.blue_live_id=[]
        for i in range(self.map_h):
            for j in range(self.map_w):
                self.env_map[i][j]=0
        # init block
        for i in range(Block):
            x=int(self.block[i,0])
            y=int(self.block[i,1])
            self.env_map[y][x]=3
        # init army information
        for i in range(self.red_num):
            # x,y,id,team,life
            a = Army(i,0,i,1,'live')
            self.red_army.append(a)
            x,y=self.red_army[i].x,self.red_army[i].y
            self.env_map[y][x]=1
            self.red_live_id.append(i)
        for i in range(self.blue_num):
            a = Army(i+1,self.map_h-1,i,2,'live')
            self.blue_army.append(a)
            x,y=self.blue_army[i].x,self.blue_army[i].y
            self.env_map[y][x] = 2
            self.blue_live_id.append(i)

    def _display_window(self):
        self.map = tk.Canvas(self,bg='white',height=self.map_h*UNIT_PIX,width=self.map_w*UNIT_PIX)
        self.map.place(x=0,y=0)
        # draw grid
        for c in range(0,self.map_w*UNIT_PIX,UNIT_PIX):
            x0,y0,x1,y1=c,0,c,self.map_h*UNIT_PIX
            self.map.create_line(x0,y0,x1,y1)
        for r in range(0,self.map_h*UNIT_PIX,UNIT_PIX):
            x0,y0,x1,y1=0,r,self.map_w*UNIT_PIX,r
            self.map.create_line(x0,y0,x1,y1)
        # draw block
        for i in range(Block):
            x = int(self.block[i,0])
            y = int(self.block[i,1])
            self.block_draw.append(self.map.create_rectangle(x * UNIT_PIX,
                        y * UNIT_PIX, (x + 1) * UNIT_PIX, (y + 1) * UNIT_PIX,
                        fill='black'))
        print(self.env_map)

        for i in range(len(self.red_army)):
            if self.red_army[i].life=='live':
                x,y=self.red_army[i].x,self.red_army[i].y
                self.red_army_draw.append(self.map.create_rectangle(x * UNIT_PIX,
                    y * UNIT_PIX, (x + 1) * UNIT_PIX,(y + 1) * UNIT_PIX, fill='red'))
        for i in range(len(self.blue_army)):
            if self.blue_army[i].life=='live':
                x,y=self.blue_army[i].x,self.blue_army[i].y
                self.blue_army_draw.append(self.map.create_rectangle(x * UNIT_PIX,
                    y * UNIT_PIX, (x + 1) * UNIT_PIX,(y + 1) * UNIT_PIX,fill='blue'))

    def move_one(self,action,team,id):
        if team==1:
            if action=='u':
                change_x,change_y=self.red_army[id].x, self.red_army[id].y-1
                if change_y<0:
                    if self.global_switch:
                        change_y=self.map_h-1
                    else:
                        change_y=0
            elif action=='d':
                change_x, change_y=self.red_army[id].x, self.red_army[id].y+1
                if change_y>=self.map_h:
                    if self.global_switch:
                        change_y=0
                    else:
                        change_y=self.map_h-1
            elif action=='l':
                change_x, change_y = self.red_army[id].x-1, self.red_army[id].y
                if change_x< 0:
                    if self.global_switch:
                        change_x = self.map_w-1
                    else:
                        change_x=0
            elif action=='r':
                change_x, change_y = self.red_army[id].x+1, self.red_army[id].y
                if change_x >= self.map_w:
                    if self.global_switch:
                        change_x = 0
                    else:
                        change_x=self.map_w-1
            elif action == 's':
                change_x, change_y = self.red_army[id].x , self.red_army[id].y
            if self.env_map[change_y][change_x] != 0:
                change_x, change_y = self.red_army[id].x, self.red_army[id].y

            self.env_map[self.red_army[id].y][self.red_army[id].x] = 0
            self.env_map[change_y][change_x]=1
            self.red_army[id].x, self.red_army[id].y = change_x, change_y

        elif team==2:
            if action=='u':
                change_x,change_y=self.blue_army[id].x, self.blue_army[id].y-1
                if change_y<0:
                    if self.global_switch:
                        change_y=self.map_h-1
                    else:
                        change_y=0
            elif action=='d':
                change_x, change_y=self.blue_army[id].x, self.blue_army[id].y+1
                if change_y>=self.map_h:
                    if self.global_switch:
                        change_y=0
                    else:
                        change_y=self.map_h-1
            elif action=='l':
                change_x, change_y = self.blue_army[id].x-1, self.blue_army[id].y
                if change_x< 0:
                    if self.global_switch:
                        change_x=self.map_w-1
                    else:
                        change_x=0
            elif action=='r':
                change_x, change_y = self.blue_army[id].x+1, self.blue_army[id].y
                if change_x >= self.map_w:
                    if self.global_switch:
                        change_x = 0
                    else:
                        change_x=self.map_w-1
            elif action=='s':
                change_x, change_y = self.blue_army[id].x , self.blue_army[id].y
            if self.env_map[change_y][change_x] != 0:
                change_x, change_y = self.blue_army[id].x, self.blue_army[id].y

            self.env_map[self.blue_army[id].y][self.blue_army[id].x] = 0
            self.env_map[change_y][change_x]=2
            self.blue_army[id].x, self.blue_army[id].y = change_x, change_y

    def move(self,action_red,action_blue):
        # random order to move agent
        order_red = []
        for i in range(len(action_red)):
            order_red.append(i)
        order_red = random.sample(order_red, len(order_red))
        order_blue = []
        for i in range(len(action_blue)):
            order_blue.append(i)
        order_blue = random.sample(order_blue, len(order_blue))

        if random.random()>0.5:
            for i in range(len(self.red_army)):
                if self.red_army[order_red[i]].life=='live':
                    self.move_one(action_red[order_red[i]],1,order_red[i])
            for i in range(len(self.blue_army)):
                if self.blue_army[order_blue[i]].life=='live':
                    self.move_one(action_blue[order_blue[i]],2,order_blue[i])
        else:
            for i in range(len(self.blue_army)):
                if self.blue_army[order_blue[i]].life=='live':
                    self.move_one(action_blue[order_blue[i]],2,order_blue[i])
            for i in range(len(self.red_army)):
                if self.red_army[order_red[i]].life=='live':
                    self.move_one(action_red[order_red[i]],1,order_red[i])

    def flash_draw(self):
        if self.draw_pic:
            for i in range(len(self.red_army_draw)):
                self.map.delete(self.red_army_draw[i])
            for i in range(len(self.blue_army_draw)):
                self.map.delete(self.blue_army_draw[i])
            for i in range(len(self.red_army)):
                if self.red_army[i].life=='live':
                    x,y=self.red_army[i].x,self.red_army[i].y
                    self.red_army_draw.append(self.map.create_rectangle(x * UNIT_PIX,
                     y * UNIT_PIX, (x + 1) * UNIT_PIX,(y + 1) * UNIT_PIX, fill='red'))
            for i in range(len(self.blue_army)):
                if self.blue_army[i].life=='live':
                    x,y=self.blue_army[i].x,self.blue_army[i].y
                    self.blue_army_draw.append(self.map.create_rectangle(x * UNIT_PIX,
                     y * UNIT_PIX, (x + 1) * UNIT_PIX,(y + 1) * UNIT_PIX, fill='blue'))

        else:
            pass

    def fight(self):
        # compute red hungry
        for i in range(len(self.red_army)):
            self.red_army[i].blood=self.red_army[i].blood-1

        # compute red win probability
        for i in range(len(self.red_army)):
            self.red_army[i].win_p=1
            if self.red_army[i].life!='live':
                pass
            else:
                x,y=self.red_army[i].x,self.red_army[i].y
                neighbor=[]
                neighbor.append([x-1,y])
                neighbor.append([x+1, y])
                neighbor.append([x , y+1])
                neighbor.append([x, y-1])
                if x==0:
                    neighbor.remove([x-1,y])
                if x==self.map_w-1:
                    neighbor.remove([x+1,y])
                if y==0:
                    neighbor.remove([x,y-1])
                if y==self.map_h-1:
                    neighbor.remove([x,y+1])
                for s in range(len(neighbor)):
                    if self.env_map[neighbor[s][1]][neighbor[s][0]]==1:
                        self.red_army[i].win_p=self.red_army[i].win_p+0
                    elif self.env_map[neighbor[s][1]][neighbor[s][0]]==2:
                        self.red_army[i].win_p = self.red_army[i].win_p - 0.25
        # compute blue win probability
        for i in range(len(self.blue_army)):
            self.blue_army[i].win_p=1
            if self.blue_army[i].life!='live':
                pass
            else:
                x,y=self.blue_army[i].x,self.blue_army[i].y
                neighbor2 = []
                neighbor2.append([x-1,y])
                neighbor2.append([x+1, y])
                neighbor2.append([x , y+1])
                neighbor2.append([x, y-1])
                if x==0:
                    neighbor2.remove([x-1,y])
                if x==self.map_w-1:
                    neighbor2.remove([x+1,y])
                if y==0:
                    neighbor2.remove([x,y-1])
                if y==self.map_h-1:
                    neighbor2.remove([x,y+1])
                for s in range(len(neighbor2)):
                    if self.env_map[neighbor2[s][1]][neighbor2[s][0]]==2:
                        self.blue_army[i].win_p=self.blue_army[i].win_p+0
                    elif self.env_map[neighbor2[s][1]][neighbor2[s][0]]==1:
                        self.blue_army[i].win_p = self.blue_army[i].win_p-0.25

    def fight_result(self):
        red_killed,blue_killed=0,0
        for i in range(len(self.red_army)):
            if self.red_army[i].life != 'live':
                pass
            else:
                x, y = self.red_army[i].x, self.red_army[i].y
                # army lost fight
                if self.red_army[i].win_p==0:
                    self.red_army[i].life = 'dead'
                    # del self.red_army[i]
                    self.env_map[y][x] = 0
                    red_killed = red_killed + 1
                if (x== 0 and y==0) or (x==self.map_w-1 and y==self.map_h-1) \
                        or (x== self.map_w-1 and y==0) or (x==0 and y==self.map_h-1):
                    if self.red_army[i].win_p==0.5:
                        self.red_army[i].life = 'dead'
                        self.env_map[y][x] = 0
                        red_killed = red_killed + 1
                elif (x==0) or (y==0) or (x==self.map_w-1) or (y==self.map_h-1):
                    if self.red_army[i].win_p == 0.25:
                        self.red_army[i].life = 'dead'
                        self.env_map[y][x] = 0
                        red_killed = red_killed + 1


            # blue fight result
        for i in range(len(self.blue_army)):
            if self.blue_army[i].life != 'live':
                pass
            else:
                x, y = self.blue_army[i].x, self.blue_army[i].y
                # army lost fight
                if self.blue_army[i].win_p==0:
                    self.blue_army[i].life = 'dead'
                    self.env_map[y][x] = 0
                    blue_killed = blue_killed + 1
                if (x == 0 and y == 0) or (x == self.map_w - 1 and y == self.map_h - 1) or \
                        (x== self.map_w-1 and y==0) or (x==0 and y==self.map_h-1):
                    if self.blue_army[i].win_p == 0.5:
                        self.blue_army[i].life = 'dead'
                        self.env_map[y][x] = 0
                        blue_killed = blue_killed + 1
                elif (x == 0) or (y == 0) or (x == self.map_w - 1) or (y == self.map_h - 1):
                    if self.blue_army[i].win_p == 0.25:
                        self.blue_army[i].life = 'dead'
                        self.env_map[y][x] = 0
                        blue_killed = blue_killed + 1

        # change number of red and blue
        del_list=[]
        for i in range(len(self.red_army)):
            if self.red_army[i].life=='dead':
                del_list.append(i)
        for i in range(len(del_list)):
            del_list[i]=del_list[i]-i
        for i in range(len(del_list)):
            del self.red_army[del_list[i]]

        del_list = []
        for i in range(len(self.blue_army)):
            if self.blue_army[i].life == 'dead':
                del_list.append(i)
        for i in range(len(del_list)):
            del_list[i] = del_list[i] - i
        for i in range(len(del_list)):
            del self.blue_army[del_list[i]]

        # hungry death for red
        del_list=[]
        for i in range(len(self.red_army)):
            if self.red_army[i].blood==0:
                x,y=self.red_army[i].x,self.red_army[i].y
                self.env_map[y][x]=0
                del_list.append(i)
        for i in range(len(del_list)):
            del_list[i]=del_list[i]-i
        for i in range(len(del_list)):
            del self.red_army[del_list[i]]

        # generate red and blue
        red_live_num=len(self.red_army)
        blue_live_num=len(self.blue_army)
        new_red_birth=min(int(0.5*blue_live_num),5)
        new_blue_birth=min(int(0.5*blue_live_num),5)

        for i in range(new_red_birth):
            x,y=random.randint(0,self.map_w-1),random.randint(0,self.map_h-1)
            if self.env_map[y][x]!=0:
                pass
            else:
                a=Army(x,y,i+red_live_num,1,'live')
                self.red_army.append(a)
                self.env_map[y][x]=1
        for i in range(new_blue_birth):
            x,y=random.randint(0,self.map_w-1),random.randint(0,self.map_h-1)
            if self.env_map[y][x]!=0:
                pass
            else:
                a=Army(x,y,i+blue_live_num,2,'live')
                self.blue_army.append(a)
                self.env_map[y][x]=2

        return red_killed,blue_killed

    def end_battle(self):
        red_lived,blue_lived=0,0
        for i in range(len(self.red_army)):
            if self.red_army[i].life=='live':
                red_lived=red_lived+1
        for i in range(len(self.blue_army)):
            if self.blue_army[i].life=='live':
                blue_lived=blue_lived+1
        return red_lived,blue_lived

    # def get_state(self):
    #     info=OutInfo(self.map_h,self.map_w,self.red_num,self.blue_num)
    #     for i in range(self.map_h):
    #         for j in range(self.map_w):
    #             info.env_map[i][j]=self.env_map[i][j]
    #     for i in range(self.red_num):
    #         if self.red_army[i].life=='live':
    #             life=1
    #         else:
    #             life=0
    #         info.red_loc[i][0],info.red_loc[i][1],info.red_loc[i][2]=self.red_army[i].x,\
    #                                               self.red_army[i].y,life
    #     for i in range(self.blue_num):
    #         if self.blue_army[i].life=='live':
    #             life=1
    #         else:
    #             life=0
    #         info.blue_loc[i][0],info.blue_loc[i][1],info.blue_loc[i][2]=self.blue_army[i].x,\
    #                                                 self.blue_army[i].y,life
    #     return info

    def step(self):
        time.sleep(0)
        self.fight()
        red_killed,blue_killed=self.fight_result()
        red_lived, blue_lived=self.end_battle()
        self.flash_draw()
        if self.draw_pic:
            self.update()

        # reward function
        if red_lived==0 and blue_lived==0:
            reward_red,reward_blue=red_lived,blue_lived
            self._init_map()
            done = True
            if red_lived!=0:
                # print('red',red_lived,blue_lived)
                pass
            else:
                # print('blue',red_lived,blue_lived)
                pass
            time.sleep(0)
        else:
            # reward_red, reward_blue=blue_killed,red_killed
            reward_red, reward_blue=0,0
            done = False
        return reward_red,reward_blue,red_killed,blue_killed,done
