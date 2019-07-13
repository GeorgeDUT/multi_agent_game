import gambit
g=gambit.Game.new_table([2,2])
g.tile="one-game"
g.players[0].label="A"
g.players[1].label="B"
print(g)
g[0,0][0]=-8
g[0,1][0]=0
g[1,0][0]=-10
g[1,1][0]=-1

g[0,0][1]=-8
g[0,1][1]=-10
g[1,0][1]=0
g[1,1][1]=-1


print(g.contingencies)
solver=gambit.nash.ExternalEnumMixedSolver()
p=solver.solve(g)
print(p)