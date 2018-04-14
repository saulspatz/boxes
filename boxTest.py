from math import factorial
import numpy as np
import sys

'''
We have a unlimited number of balls numbered 0,1,...,n-1.
One ball of each color is placed in a box, and a ball is drawn at random.  
If the ball drawn is numbered k, it is replaced by a ball numbered
k+1 (mod n).  The process is repareated until all the balls in the box 
have the same number.  What is the expected number of draws? 
'''
def binomial(n,k):
    return factorial(n)//factorial(k)//factorial(n-k)

def states(n):
    return compositions(n,n)

def compositions(n,m):
    '''
    Compositions of n into m nonnegative parts
    '''
    if m==0: return ( )
    if m==1: return [(n,)]
    if n==0: return [m*(0,)]
    answer = []
    for k in range(n+1):
        answer.extend([(k,)+c for c in compositions(n-k, m-1)])
    return answer

def children(box, n):
    '''
    box is the current stated of the box
    box[k] is the number of balls numbered k in the box
    
    return value is a list of pairs (state, m)
    where state is the child state and m is multiplicity
    '''
    if max(box) ==n:
        return [(box,n)]
    answer = []
    bx=list(box)
    for k in range(n-1):
        if bx[k]==0: continue
        c1 = bx[:k+1]
        c2 = bx[k+1:]
        c1[-1]-=1
        c2[0]+=1
        answer.append((tuple(c1+c2), box[k]))
    if bx[-1]:
        c=bx[:]
        c[0]+= 1
        c[-1]-=1
        answer.append((tuple(c), box[-1]))
    return answer

for n in range(3,4):
    N = binomial(2*n-1, n-1) # number of states by "stars and bars"
    #boxes = states(n)
    #boxes.sort(key=lambda x:max(x))
    boxes=[(1,1,1),
                (0,1,2),
                (1,2,0),
                (2,0,1),
                (0,2,1),
                (1,0,2),
                (2,1,0),
                (0,0,3),
                (3,0,0),
                (0,3,0)
    ]
    print(boxes)
    boxes = {b:i for i,b in enumerate(boxes)}
    P=np.zeros((N,N), dtype = float)
    for b in boxes:
        i = boxes[b]
        for c,m in children(b,n):
            j = boxes[c]
            P[i,j] += m
    P /= n
    trans = N-n  # number of transient states
    Q= P[:trans, :trans]
    print(Q)
    I = np.eye(trans)
    N=np.linalg.inv(I-Q)
    one = np.ones(31)
    start = boxes[n*(1,)]
    wait=sum(N.transpose())[start]
    print(n, wait)
