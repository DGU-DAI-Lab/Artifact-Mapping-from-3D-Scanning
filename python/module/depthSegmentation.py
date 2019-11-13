#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ====================================================
# 
# Module : 3D Depth Segmentation
#
# Written by hepheir@gmail.com
# Last updated : Oct 27 2019
#
# ====================================================
#
#  Process order
#
#  1. Breakage mesh : (3D, 3D, 3D)
#    1-1. Sort facets into front, slice, or rear areas.
#
#  2. Cutting mesh : (3D, 2D, 3D)
#    2-1. Separate each facet in slice area (after breakage)
#         into 1 line, and 2 small facets
#
# ====================================================

from stl import mesh
import stl
import numpy as np

# ====================================================

def macro(obj):
    assert isinstance(obj,mesh.Mesh)
    breakage = _breakage(obj)
    cutting  = _cutting(breakage)
    return np.array(cutting)

# ====================================================

def _breakage(obj):
    z = obj.z
    n = obj.normals
    front,section_breakage,rear = [],[],[]

    for i in range(obj.__len__()):
        # Front or behind the xy-surface
        isFront = isRear = False
        for _z in z[i]:
            isFront |= (_z >= 0)
            isRear  |= (_z <= 0)
        #  - Find slices
        if isFront and isRear:
            section_breakage.append(obj.data[i])
        #  - Find fronts and behinds
        elif n[i,2] > 0:
            if isFront:
                front.append(obj.data[i])
            if isRear:
                rear.append(obj.data[i])
    return front,section_breakage,rear

def _cutting(breakage):
    """breakage 과정에서 section으로 분류된 facet의 후처리.
    - 단면에 걸치는 Facet을 모두 단면을 따라 정밀하게 3분할 및 front/rear로의 재분배.
    - 처리 이후 section에는 facet data가 아닌 2D 선분정보만 남게 됨.
    (front와 rear의 데이터형식은 변화없음.)"""

    def where_z_is_0(v0,v1):
        """두 벡터가 이루는 선분 상에서 z=0인 점을 계산."""
        x0,y0,z0 = v0
        x1,y1,z1 = v1
        x = (x0*z1 - x1*z0) / (z1 - z0)
        y = (y0*z1 - y1*z0) / (z1 - z0)
        return [x,y,0]

    front, section_breakage, rear = breakage
    section_cutting = []

    new_data = new_vectors = None
    i = j = k = A = B = C = z = None

    for normal,vectors,attr in section_breakage:
        z = vectors[:, 2]

        if np.prod(z) == 0:
            # Pattern (a), (b) or (c)
            # TODO
            print('found 0')
            continue

        else:
            # Pattern (e)
            for i in [0,1,2]:
                if (z[i] * z[(i+1)%3] > 0): break
            j = (i+1)%3
            k = (i+2)%3

            B = where_z_is_0(vectors[j],vectors[k])
            C = where_z_is_0(vectors[k],vectors[i])

            if B[:2] == C[:2]:
                # Meaningless to append a dot.
                continue

            section_cutting.append((B[0],B[1],C[0],C[1]))

            new_vectors = np.array([ # Create new reference : no need to .copy()
                [ vectors[i], vectors[j], B         ],
                [ vectors[i], B         , C         ],
                [ C         , B         , vectors[k]]]) # opp.

        if normal[2] > 0: # if Visible
            n_of_vectors = len(new_vectors)
            new_data = np.zeros(n_of_vectors, dtype=mesh.Mesh.dtype)
            new_data['vectors'] = new_vectors
            new_data['normals'] = [ normal ] * n_of_vectors
            new_data['attr']    = [ attr ]   * n_of_vectors

            for i in range(n_of_vectors):
                if np.sum(new_vectors[:,2]) > 0:
                    front.append(new_data[i])
                else:
                    rear.append(new_data[i])
    return front, section_cutting, rear