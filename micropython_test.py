import math
# test dumb micropython


print(dir(math))
print("micropython test .... run and than run away")
print(math.copysign(2, -1))
v = -1
# v = math.copysign(min(math.abs(v), 255), v)
print(math.fabs(-20))
print(math.fabs(20))
