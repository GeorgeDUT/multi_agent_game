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


MAP_W = 6
MAP_H = 6
UNIT_PIX = 17
R_ARMY_NUM = 4
B_ARMY_NUM = 4
Block=0

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
        # generation block
        self.block = np.zeros((Block, 2))
        for i in range(Block):
            self.block[i, 0] = random.randint(0, self.map_w - 2)
            self.block[i, 1] = random.randint(2, self.map_h - 2)

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
        for i in range(self.map_h):
            for j in range(self.map_w):
                self.env_map[i][j]=0
        # init block
        for i in range(Block):
            x=int(self.block[i,0])
            y=int(self.block[i,1])
            self.env_map[y][x]=3
        # init army information
        print(self.red_num)
        for i in range(self.red_num):
            # x,y,id,team,life
            a = Army(i,0,i,1,'live')
            self.red_army.append(a)
            x,y=self.red_army[i].x,self.red_army[i].y
            self.env_map[y][x]=1
        for i in range(self.blue_num):
            a = Army(i,self.map_h-1,i,2,'live')
            self.blue_army.append(a)
            x,y=self.blue_army[i].x,self.blue_army[i].y
            self.env_map[y][x] = 2

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

        # draw agent
        for i in range(self.red_num):
            if self.red_army[i].life=='live':
                x,y=self.red_army[i].x,self.red_army[i].y
                self.red_army_draw.append(self.map.create_rectangle(x * UNIT_PIX,
                    y * UNIT_PIX, (x + 1) * UNIT_PIX,(y + 1) * UNIT_PIX, fill='red'))
        for i in range(self.blue_num):
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
            for i in range(self.red_num):
                if self.red_army[order_red[i]].life=='live':
                    self.move_one(action_red[order_red[i]],1,order_red[i])
            for i in range(self.blue_num):
                if self.blue_army[order_blue[i]].life=='live':
                    self.move_one(action_blue[order_blue[i]],2,order_blue[i])
        else:
            for i in range(self.blue_num):
                if self.blue_army[order_blue[i]].life=='live':
                    self.move_one(action_blue[order_blue[i]],2,order_blue[i])
            for i in range(self.red_num):
                if self.red_army[order_red[i]].life=='live':
                    self.move_one(action_red[order_red[i]],1,order_red[i])

    def flash_draw(self):
        if self.draw_pic:
            for i in range(len(self.red_army_draw)):
                self.map.delete(self.red_army_draw[i])
            for i in range(len(self.blue_army_draw)):
                self.map.delete(self.blue_army_draw[i])
            for i in range(self.red_num):
                if self.red_army[i].life=='live':
                    x,y=self.red_army[i].x,self.red_army[i].y
                    self.red_army_draw.append(self.map.create_rectangle(x * UNIT_PIX,
                     y * UNIT_PIX, (x + 1) * UNIT_PIX,(y + 1) * UNIT_PIX, fill='red'))
            for i in range(self.blue_num):
                if self.blue_army[i].life=='live':
                    x,y=self.blue_army[i].x,self.blue_army[i].y
                    self.blue_army_draw.append(self.map.create_rectangle(x * UNIT_PIX,
                     y * UNIT_PIX, (x + 1) * UNIT_PIX,(y + 1) * UNIT_PIX, fill='blue'))

        else:
            pass

    def fight(self):
        # compute red win probability
        for i in range(self.red_num):
            self.red_army[i].win_p=1
            if self.red_army[i].life!='live':
                pass
            else:
                x,y=self.red_army[i].x,self.red_army[i].y
                qi=4
                red=0
                blue=0
                if x==0:
                    qi=qi-1
                if y==0:
                    qi=qi-1
                if x==self.map_w-1:
                    qi=qi-1
                if y==self.map_h-1:
                    qi=qi-1
                add_xy=[[1,0],[-1,0],[0,1],[0,-1]]
                for num in range(4):
                   nex,ney=x+add_xy[num][0],y+add_xy[num][1]
                   if nex<0:
                       nex=0
                   if ney<0:
                       ney=0
                   if nex>self.map_w-1:
                       nex=self.map_w-1
                   if ney>self.map_h-1:
                       ney=self.map_h-1
                   if self.env_map[ney][nex]==1:
                       qi=qi
                       red=red+1
                   elif self.env_map[ney][nex]==2:
                       qi=qi-1
                       blue=blue+1
                   elif self.env_map[ney][nex]==3:
                       qi=qi-1
                if qi==0:
                    self.red_army[i].win_p=0
                else:
                    self.red_army[i].win_p =1
        # compute blue win probability
        for i in range(self.blue_num):
            self.blue_army[i].win_p=1
            if self.blue_army[i].life!='live':
                pass
            else:
                x,y=self.blue_army[i].x,self.blue_army[i].y
                qi = 4
                red=0
                blue=0
                if x==0:
                    qi=qi-1
                if y==0:
                    qi=qi-1
                if x==self.map_w-1:
                    qi=qi-1
                if y==self.map_h-1:
                    qi=qi-1
                add_xy=[[1,0],[-1,0],[0,1],[0,-1]]
                for num in range(4):
                   nex,ney=x+add_xy[num][0],y+add_xy[num][1]
                   if nex<0:
                       nex=0
                   if ney<0:
                       ney=0
                   if nex>self.map_w-1:
                       nex=self.map_w-1
                   if ney>self.map_h-1:
                       ney=self.map_h-1
                   if self.env_map[ney][nex]==1:
                       qi=qi-1
                       red=red+1
                   elif self.env_map[ney][nex]==2:
                       qi=qi
                       blue=blue+1
                   elif self.env_map[ney][nex]==3:
                       qi=qi-1

                if qi == 0:
                    self.blue_army[i].win_p = 0
                else:
                    self.blue_army[i].win_p =1

    def fight_result_pro(self):
        red_killed,blue_killed=0,0
        for i in range(self.red_num):
            if self.red_army[i].life != 'live':
                pass
            else:
                x, y = self.red_army[i].x, self.red_army[i].y
                win_rate=random.uniform(0,1)
                if win_rate>self.red_army[i].win_p:
                    self.red_army[i].life='dead'
                    self.env_map[y][x]=0
                    red_killed = red_killed + 1
                    print("red_dead",win_rate)

        for i in range(self.blue_num):
            if self.blue_army[i].life != 'live':
                pass
            else:
                x, y = self.blue_army[i].x, self.blue_army[i].y
                win_rate=random.uniform(0,1)
                if win_rate>self.blue_army[i].win_p:
                    self.blue_army[i].life='dead'
                    self.env_map[y][x]=0
                    blue_killed = blue_killed + 1
                    print("blue_dead",win_rate)
        return red_killed, blue_killed

    def end_battle(self):
        red_lived,blue_lived=0,0
        for i in range(self.red_num):
            if self.red_army[i].life=='live':
                red_lived=red_lived+1
        for i in range(self.blue_num):
            if self.blue_army[i].life=='live':
                blue_lived=blue_lived+1
        return red_lived,blue_lived

    def get_state(self):
        info=OutInfo(self.map_h,self.map_w,self.red_num,self.blue_num)
        for i in range(self.map_h):
            for j in range(self.map_w):
                info.env_map[i][j]=self.env_map[i][j]
        for i in range(self.red_num):
            if self.red_army[i].life=='live':
                life=1
            else:
                life=0
            info.red_loc[i][0],info.red_loc[i][1],info.red_loc[i][2]=self.red_army[i].x,\
                                                  self.red_army[i].y,life
        for i in range(self.blue_num):
            if self.blue_army[i].life=='live':
                life=1
            else:
                life=0
            info.blue_loc[i][0],info.blue_loc[i][1],info.blue_loc[i][2]=self.blue_army[i].x,\
                                                    self.blue_army[i].y,life
        return info

    def step(self):
        time.sleep(0.1)
        self.fight()
        red_killed,blue_killed=self.fight_result_pro()
        red_lived, blue_lived=self.end_battle()
        self.flash_draw()
        if self.draw_pic:
            self.update()

        # reward function
        if red_lived==0 or blue_lived==0:
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
