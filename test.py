import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

s=[]

for i in range(100):
    noise=np.random.uniform(0,0.025)
    a,b,c=0.000205,0.039,0.059
    d,e,f=0.18,0.38,0.4
    s.append(0)
    if i==0:
        s[i]=0
    if 1<=i<=3:
        s[i]=a
    if 4<=i<=9:
        s[i]=a+0.0048*(i-4)
    if 10<=i<=15:
        s[i]=b
    if 16<=i<=30:
        s[i]=b+0.0034*(i-16)
    if 31 <= i <= 40:
        s[i] = c + 0.0074*(i-31)
    if 41<=i<=55:
        s[i]=d+0.00701*(i-41)
    if 55<=i<=60:
        s[i]=d+0.1+0.00501*(i-55)
    if 60<=i<=65:
        s[i]=d+0.15+0.00501*(i-60)
    if 66<=i<=80:
        s[i]=e+0.001*(i-66)
    if 81<=i<=91:
        s[i]=e+0.0012*(i-81)
    if 92<=i<=100:
        s[i]=f+0.0009*(i-92)
    s[i]=s[i]+noise

plt.plot(s,color='r')
plt.show()


