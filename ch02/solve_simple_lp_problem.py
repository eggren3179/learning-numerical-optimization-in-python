"""
120x + 150y = 1440
x + y = 10
の単純な線形1次連立方程式を解くプログラム
"""

import pulp

problem = pulp.LpProblem('SLE', pulp.LpMaximize)

x = pulp.LpVariable('x', cat='Continuous')
y = pulp.LpVariable('y', cat='Continuous')

problem += 120 * x + 150 * y == 1440
problem += x + y == 10

status = problem.solve()

print(f"Status:{pulp.LpStatus[status]}")
print(f"x = {x.value()}, y = {y.value()}")