from stl import mesh
import numpy as np

obj = mesh.Mesh.from_file('../토기 예시 데이터/3D 스캔 파일/토기1.stl')

i = 0
l = len(obj.vectors)

considers = []
for vect in obj.vectors:
    behind = front = False
    direction = np.cross(np.subtract(vect[0],vect[1]), np.subtract(vect[0],vect[2]))
    for x,y,z in vect:
        front  |= (x >= 0)
        behind |= (x <= 0)
    if front and behind:
        considers.append(vect)
    i += 1
    print("\r%d/%d"%(i,l), end="")
print(considers)