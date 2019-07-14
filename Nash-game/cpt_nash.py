import gambit
import numpy as np

g=gambit.Game.new_table([2,2,2])
print(len(g.players))
g.tile="one-game"
g.players[0].label="A"
g.players[1].label="B"
print(g)
g[0,0,0][0]=1
g[0,1,0][0]=-1
g[1,0,0][0]=-1
g[1,1,0][0]=1
g[0,0,1][0]=1
g[0,1,1][0]=-1
g[1,0,1][0]=1
g[1,1,1][0]=0


g[0,0,0][1]=-1
g[0,1,0][1]=1
g[1,0,0][1]=1
g[1,1,0][1]=-1
g[0,0,1][1]=-1
g[0,1,1][1]=1
g[1,0,1][1]=0
g[1,1,1][1]=0

g[0,0,0][2]=10
g[0,1,0][2]=-10
g[1,0,0][2]=0
g[1,1,0][2]=-1
g[0,0,1][2]=-8
g[0,1,1][2]=-10
g[1,0,1][2]=0
g[1,1,1][2]=-9

g[0,0,0][2]=8
g[0,1,0][2]=0
g[1,0,0][2]=-10
g[1,1,0][2]=-1
g[0,0,1][2]=0
g[0,1,1][2]=0
g[1,0,1][2]=-1
g[1,1,1][2]=10

g[0,0,0][2]=0
g[0,1,0][2]=0
g[1,0,0][2]=0
g[1,1,0][2]=0
g[0,0,1][2]=-10
g[0,1,1][2]=10
g[1,0,1][2]=-10
g[1,1,1][2]=10

print('action',list(g.contingencies))
solver=gambit.nash.ExternalGlobalNewtonSolver()
p=solver.solve(g)
print(p)
print(len(p))
for i in range(len(p)):
    print(p[i])
for i in range(len(p)):
    print(p[i][4])

print("pure nash")
p2=gambit.nash.enumpure_solve(g)
print(p2)
