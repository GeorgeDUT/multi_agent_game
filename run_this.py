from war_1 import *
import tensorflow as tf


def update():
    while(1):
        a= []
        for i in range(4):
            action=np.random.choice(['u','d','r','l','s'])
            a.append(action)
        my_map.move(a, a[1])
        my_map.step()
        

if __name__ == "__main__":
    print ('war!')
    my_map = WarMap(10,5,4,1,True)
    my_map.after(10,update)
    my_map.mainloop()