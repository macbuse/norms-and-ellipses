import matplotlib.pyplot as plt
from math import cos,sin,pi

import numpy as np



def mk_vectors():
    def cc(t):
        return np.array([cos(t*np.pi/180),sin(t*np.pi/180)])
    
    angle_offset = 10
    u = cc(0 + angle_offset )
    v = cc(120 + angle_offset )
    #w = cc(100 + angle_offset )
    return [u,v,cc(240 + angle_offset )]

class Norm(object):
    '''norm given by a finite set of seminorms
    i.e. dot products with a finite set of vectors
    L = list of vectors'''
    
    def __init__(self,L):
        L.extend([-v for v in L])
        L.sort(key = lambda v : np.arctan2(v[0],v[1]))
        self.L = L
        
        self.face_vectors = np.array([ v/self.value(v) for v in self.L])
        
        L.append(L[0])
        LL = [u - v for u,v in zip(L,L[1:])]
        LL = [ np.array([ -x[1], x[0] ]) for x in LL]
        self.vert_vectors = [ v/self.value(v) for v in LL]
        
        
    def value(self,x):
        return max([abs(np.dot(x,y)) for y in self.L])
    
    def dist(self,x,y):
        return self.value(x-y)
    

def dichotomy(a,fn):
    '''basic implementation of a root search
    by dichotomy method'''
    b = np.array([0,0])
    if fn(b) > 0 : return b
    while np.linalg.norm(b-a) > .01:
        #k += 1
        c = .5*(a+b)
        if fn(c)*fn(a) < 0:
            a,b = a,c
        else:
            a,b = c,b
    return b

    

def draw(L, col = '#eeefff'):
    xs = [x[0] for x in L]
    ys = [x[1] for x in L]
    plt.plot(xs,ys, color = col)
    

#instantiate the norm object
#mnorm is global to some of the  functions above

mnorm = Norm(mk_vectors() )

pt0 = np.array([0,0])
circ = [ np.array([ cos(t), sin(t)] ) for t in np.linspace(0,2*np.pi,100) ]

ball = [ dichotomy(5*x, lambda a: mnorm.dist(a, pt0)  - 1) for x in circ]

draw(ball, col = '#FF0000')
draw([x + np.array([2,0]) for x in ball],col = '#FF0000')



pt1,pt2 = np.array([-1,0]), np.array([1,0])


from scipy.spatial import ConvexHull
pt1 = 0*pt1
def mk_ellipse(f1,f2,R ):
    
    distance = mnorm.dist
    LL = mnorm.vert_vectors
   
    ellipse  =  [ dichotomy(5*x, lambda a: distance(a, f1) + distance(a, f2) - R) for x in LL]
    ellipse.extend(
            [ pt2 + dichotomy(5*x, lambda a: distance(a, - f2) + distance(a, f1) - R) for x in LL] ) 
    
    ellipse = np.array(ellipse)
    hull = ConvexHull(ellipse)
    
    for simplex in hull.simplices:
        plt.plot(ellipse[simplex, 0], ellipse[simplex, 1], 'b-')


xs,ys = mnorm.face_vectors.transpose()
plt.plot(xs,ys, '#FF00FF')
        
def vert_vectors(pt):
    for v in mnorm.vert_vectors :
        u = 2*v + pt
        plt.plot([pt[0],u[0]],
                 [pt[1],u[1]], '-g' )
        u = v + pt
        plt.plot([pt[0],u[0]],
                 [pt[1],u[1]], 'og' )
               
for x  in pt1,pt2:
    plt.plot(x[0],x[1], 'x', color = 'b')
 
pt1 = np.array([0,0])
pt2 = np.array([2,0])

vert_vectors(pt2)
vert_vectors(pt1)

for length in np.linspace(2.01,5,8):
    mk_ellipse(pt1,pt2,length)

NN = 3
plt.xlim(-2,NN)
plt.ylim(-2,NN)
plt.axes().set_aspect('equal', 'datalim')

plt.show()
