"""
war_1 game is multi_agent war game, red_army vs blue_army
turn-based strategy game
rule:
    1,every turn agent move first,red or blue move first,from 1 to n, then fight, then judge fight result.
    2,the more agent in fight, the higher probability win.
    3,every agent in every turn can only do one action.

function list:
    my_map = WarMap(w,h,red,blue,tk_draw)
# new a WarMap class, size w*h, agent num red, blue, if tk_draw False, then do not draw picture.
    mp_map.move(action_red[],action_blue[])
# red_army action list, blue_army action list. action space {u,d,l,r,s}
    mp_map.step()
# return reward_red, reward_blue, done.
    my_map.get_state()
# return map

About WarMap
red and blue fight each other, red can be killed,
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

print('this is war_1: fight')


class Army(object):
    def __init__(self,x=0,y=0,id=0,team=0,life='live'):
        self.x=x
        self.y=y
        self.id=id
        self.team=team
        self.life=life
        self.win_p=1


class OutInfo(object):
    def __init__(self, h, w, red_num, blue_num):
        self.env_map=np.zeros(shape=(h,w))
        self.red_num=red_num
        self.blue_num=blue_num
        self.army_loc=np.zeros((red_num+blue_num)*4)
        self.feature_stat=np.zeros(int(math.pow(2,blue_num)))


class WarMap(tk.Tk, object):
    def __init__(self, w=MAP_W, h=MAP_H, red=R_ARMY_NUM, blue=B_ARMY_NUM, draw_pic=False):
        self.draw_pic = draw_pic
        self.map_w = w
        self.map_h = h
        self.red_num = red
        self.blue_num = blue
        # env_map = 0, space, =1,red_army, =2, blue_army
        self.env_map = np.zeros(shape=(self.map_h, self.map_w))
        self.red_army = []
        self.blue_army = []
        self.red_army_draw=[]
        self.blue_army_draw=[]

        self._init_map()

        if draw_pic:
            super(WarMap,self).__init__()
            self.title('war_1 game')
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
        # init army information
        for i in range(self.red_num):
            a = Army(i,0,i,1,'live')
            self.red_army.append(a)
            x,y=self.red_army[i].x,self.red_army[i].y
            self.env_map[y][x]=1
        for i in range(self.blue_num):
            a = Army(i+1,self.map_h-3,i,2,'live')
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
        # draw agent
        for i in range(self.map_h):
            for j in range(self.map_w):
                if self.env_map[i][j]==1:
                    self.red_army_draw.append(self.map.create_rectangle(j*UNIT_PIX,
                    i*UNIT_PIX,(j+1)*UNIT_PIX,(i+1)*UNIT_PIX,fill='red'))
                elif self.env_map[i][j]==2:
                    self.blue_army_draw.append(self.map.create_rectangle(j * UNIT_PIX,
                                                                   i * UNIT_PIX, (j + 1) * UNIT_PIX, (i + 1) * UNIT_PIX,
                                                                   fill='blue'))

    def move_one(self,action,team,id):
        if team==1:
            if action=='u':
                change_x,change_y=self.red_army[id].x, self.red_army[id].y-1
                if change_y<0:
                    change_y=0
            elif action=='d':
                change_x, change_y=self.red_army[id].x, self.red_army[id].y+1
                if change_y>=self.map_h:
                    change_y=self.map_h-1
            elif action=='l':
                change_x, change_y = self.red_army[id].x-1, self.red_army[id].y
                if change_x< 0:
                    change_x = 0
            elif action=='r':
                change_x, change_y = self.red_army[id].x+1, self.red_army[id].y
                if change_x >= self.map_w:
                    change_x = self.map_w - 1
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
                    change_y=0
            elif action=='d':
                change_x, change_y=self.blue_army[id].x, self.blue_army[id].y+1
                if change_y>=self.map_h:
                    change_y=self.map_h-1
            elif action=='l':
                change_x, change_y = self.blue_army[id].x-1, self.blue_army[id].y
                if change_x< 0:
                    change_x = 0
            elif action=='r':
                change_x, change_y = self.blue_army[id].x+1, self.blue_army[id].y
                if change_x >= self.map_w:
                    change_x = self.map_w - 1
            elif action=='s':
                change_x, change_y = self.blue_army[id].x , self.blue_army[id].y
            if self.env_map[change_y][change_x] != 0:
                change_x, change_y = self.blue_army[id].x, self.blue_army[id].y
            self.env_map[self.blue_army[id].y][self.blue_army[id].x] = 0
            self.env_map[change_y][change_x]=2
            self.blue_army[id].x, self.blue_army[id].y = change_x, change_y

    def move(self,action_red,action_blue):
        if random.random()>0.5:
            for i in range(self.red_num):
                if self.red_army[i].life=='live':
                    self.move_one(action_red[i],1,i)
            for i in range(self.blue_num):
                if self.blue_army[i].life=='live':
                    self.move_one(action_blue[i],2,i)
        else:
            for i in range(self.blue_num):
                if self.blue_army[i].life=='live':
                    self.move_one(action_blue[i],2,i)
            for i in range(self.red_num):
                if self.red_army[i].life=='live':
                    self.move_one(action_red[i],1,i)

    def flash_draw(self):
        if self.draw_pic:
            for i in range(len(self.red_army_draw)):
                self.map.delete(self.red_army_draw[i])
            for i in range(len(self.blue_army_draw)):
                self.map.delete(self.blue_army_draw[i])
            for i in range(self.map_h):
                for j in range(self.map_w):
                    if self.env_map[i][j]==1:
                        self.red_army_draw.append(self.map.create_rectangle(j*UNIT_PIX,
                        i*UNIT_PIX,(j+1)*UNIT_PIX,(i+1)*UNIT_PIX,fill='red'))
                    elif self.env_map[i][j]==2:
                        self.blue_army_draw.append(self.map.create_rectangle(j * UNIT_PIX,
                                                                   i * UNIT_PIX, (j + 1) * UNIT_PIX, (i + 1) * UNIT_PIX,
                                                                   fill='blue'))
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
                        self.red_army[i].win_p=self.red_army[i].win_p+0.25/3
                    elif self.env_map[neighbor[s][1]][neighbor[s][0]]==2:
                        self.red_army[i].win_p = self.red_army[i].win_p - 0.25
        # compute blue win probability
        for i in range(self.blue_num):
            self.blue_army[i].win_p=1
            if self.blue_army[i].life!='live':
                pass
            else:
                x,y=self.blue_army[i].x,self.blue_army[i].y
                neighbor2=[]
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
                        self.blue_army[i].win_p=self.blue_army[i].win_p+0.25/3
                    elif self.env_map[neighbor2[s][1]][neighbor2[s][0]]==1:
                        self.blue_army[i].win_p = self.blue_army[i].win_p-0.25

    def fight_result(self):
        red_killed,blue_killed=0,0
        # red fight result
        for i in range(self.red_num):
            if self.red_army[i].life!='live':
                pass
            else:
                win_pro=random.random()
                x,y=self.red_army[i].x,self.red_army[i].y
                # army lost fight
                if win_pro>self.red_army[i].win_p:
                    self.red_army[i].life='dead'
                    self.env_map[y][x]=0
                    red_killed=red_killed+1
        # blue fight result
        for i in range(self.blue_num):
            if self.blue_army[i].life!='live':
                pass
            else:
                win_pro=random.random()
                x,y=self.blue_army[i].x,self.blue_army[i].y
                # army lost fight
                if win_pro>self.blue_army[i].win_p:
                    self.blue_army[i].life='dead'
                    self.env_map[y][x]=0
                    blue_killed=blue_killed+1
        return red_killed,blue_killed

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
        for i in range(info.red_num):
            if self.red_army[i].life!='live':
                x,y,id,team=-1,-1,1,1
            else:
                x,y,id,team=self.red_army[i].x,self.red_army[i].y,i,1
            info.army_loc[i*4],info.army_loc[i*4+1],info.army_loc[i*4+2],info.army_loc[i*4+3]=x,y,id,team
        for i in range(info.blue_num):
            if self.blue_army[i].life!='live':
                x, y, id, team = -1, -1, 1, 1
            else:
                x, y, id, team = self.blue_army[i].x,self.blue_army[i].y,i,2
                info.army_loc[(i+self.red_num)*4+0], info.army_loc[(i+self.red_num)*4+1], \
                info.army_loc[(i+self.red_num)*4+2], info.army_loc[(i+self.red_num)*4+3]=x,y,id,team
        '''change state info'''
        for i in range(self.blue_num):
            if self.blue_army[i].life=='live':
                info.feature_stat[i]=1
            else:
                info.feature_stat[i]=0
        return info

    def step(self):
        time.sleep(0)
        self.fight()
        red_killed,blue_killed=self.fight_result()
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
                #print('red',red_lived,blue_lived)
                pass
            else:
                #print('blue',red_lived,blue_lived)
                pass
            time.sleep(0)
        else:
            # reward_red, reward_blue=blue_killed,red_killed
            reward_red, reward_blue=0,0
            done = False
        return reward_red,reward_blue,done
