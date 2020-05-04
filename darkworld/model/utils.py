class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


'''
finding intersect point of line AB and CD 
where A is the first point of line AB
and B is the second point of line AB
and C is the first point of line CD
and D is the second point of line CD
'''



def get_intersect(A, B, C, D):
    # a1x + b1y = c1
    a1 = B.y - A.y
    b1 = A.x - B.x
    c1 = a1 * (A.x) + b1 * (A.y)

    # a2x + b2y = c2
    a2 = D.y - C.y
    b2 = C.x - D.x
    c2 = a2 * (C.x) + b2 * (C.y)

    # determinant
    det = a1 * b2 - a2 * b1

    # parallel line
    if det == 0:
        return (float('inf'), float('inf'))

    # intersect point(x,y)
    x = ((b2 * c1) - (b1 * c2)) / det
    y = ((a1 * c2) - (a2 * c1)) / det
    return (x, y)

def get_intersect_AB(A, B, C, D):

    ax,ay = A
    bx,by = B
    cx,cy = C
    dx,dy = D

    # a1x + b1y = c1
    a1 = by - ay
    b1 = ax - bx
    c1 = a1 * (ax) + b1 * (ay)

    # a2x + b2y = c2
    a2 = dy - cy
    b2 = cx - dx
    c2 = a2 * (cx) + b2 * (cy)

    # determinant
    det = a1 * b2 - a2 * b1

    # parallel line
    if det == 0:
        return (float('inf'), float('inf'))

    # intersect point(x,y)
    x = ((b2 * c1) - (b1 * c2)) / det
    y = ((a1 * c2) - (a2 * c1)) / det
    return (x, y)