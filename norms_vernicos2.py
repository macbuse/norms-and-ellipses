import matplotlib.pyplot as plt
import numpy as np

'''implements class for doing calculations with polygonal norms'''


def mk_vectors():
    def cc(t):
        return np.array([np.cos(t*np.pi/180),np.sin(t*np.pi/180)])
    
    angle_offset = 40
    u = cc(0 + angle_offset )
    v = cc(120 + angle_offset )
    #w = cc(100 + angle_offset )
    
    return [ cc(angle_offset), cc(90 + angle_offset)]
    return [u,cc(240 + angle_offset), v]

class Norm(object):
    '''norm given by a finite set of seminorms
    i.e. dot products with a finite set of vectors
    L = list of vectors'''
    
    def __init__(self,L):
        #symmetrize and order the vectors (anti-clockwise)
        L.extend([-v for v in L])
        L.sort(key = lambda v : np.arctan2(v[0],v[1]))
        self.L = L
        self.face_vectors = np.array([ v/self.value(v) for v in self.L])
        
        #calculate the dual vectors
        #no need to reorder these
        L.append(L[0])
        LL = [u - v for u,v in zip(L,L[1:])]
        LL = [ np.array([ -x[1], x[0] ]) for x in LL]
        LL.append(LL[0])
        self.vert_vectors = np.array([ v/self.value(v) for v in LL])
        
        
    def value(self,vector):
        return max([abs(np.dot(vector,u )) for u in self.L])
    
    def dist(self,x,y):
        return self.value(x-y)
    
    def ellipse(self,f1,f2,R ):
        #hash these methods
        distance = self.dist
        LL = self.vert_vectors
        
        #make sure you take the initial point of dichotomy() far enough out
        #R*x seems good enough
        key_pts =  [ dichotomy(R*x, lambda a: distance(a,f1) + distance(a,f2) - R) for x in LL]
        key_pts.extend(
                [ pt2 + dichotomy(R*x, lambda a: distance(a, -f2) + distance(a,f1) - R) for x in LL] ) 
              
        #this is a hack
        #I know that the points are on the boundary of a convex set
        #and that the focus f1 is inside so all I have to do is to order them
        
        key_pts.sort(key = lambda v : np.arctan2(v[0] - f1[0] ,v[1] - f1[0]))
        key_pts.append(key_pts[0])
        return key_pts  

def dichotomy(a,fn):
    '''basic implementation of a root search
    by dichotomy method'''
    
    b = np.array([0,0])
    if fn(b) > 0 : return b
    while np.linalg.norm(b - a) > .01:
        #k += 1
        c = .5*(a + b)
        if fn(c)*fn(a) < 0:
            a,b = a,c
        else:
            a,b = c,b
    return b

    
def draw(L, col = '#eeefff'):
    if isinstance(L,list):
        xs, ys = np.array(L).transpose()
    else:
        xs, ys = L.transpose()
    plt.plot(xs,ys, color = col)
    
#instantiate the norm object
#mnorm is global to some of the  functions above

mnorm = Norm(mk_vectors() )

def vert_vectors(pt):
    draw( mnorm.vert_vectors + pt, '#FF0000')
    
    for v in mnorm.vert_vectors :
        u = 10*v + pt
        plt.plot([pt[0],u[0]],
                 [pt[1],u[1]], '-g' )
        u = v + pt
        plt.plot([u[0]],
                 [u[1]], 'or' )
               
pt1 = np.array([0,0])
pt2 = np.array([2,1])

focal_dist = np.linalg.norm(pt2 - pt1)
for length in np.linspace(focal_dist , 5*focal_dist , 32):
    draw( mnorm.ellipse(pt1,pt2,length),
          col = '#0000ff')

#draw the distance balls   
vert_vectors(pt2)
vert_vectors(pt1)

for x  in pt1,pt2:
    plt.plot(x[0],x[1], 'xb')

draw(mnorm.face_vectors, '#FF00FF')
    
#set up bounding box etc.
plt.xlim(-2,5)
plt.ylim(-3,3)
plt.axes().set_aspect('equal', 'datalim')

plt.show()
