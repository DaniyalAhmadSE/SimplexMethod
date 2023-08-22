a = ['x1', 'x2', 'S1', 'S2', 'S3', 'R1', 'R2']

b = ['R1', 'S2', 'R2']

c = [x for x in a if x not in b]
print(c)
