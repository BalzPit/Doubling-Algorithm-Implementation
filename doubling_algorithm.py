
"""
Created on Sun Jan 10 16:51:44 2021

@author: pitba
"""
import math
import random
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import distance
from numpy.random import default_rng
import linecache

N = 5000
k = 15
alpha = 2
beta = 2
pointsx = []
pointsy = []
#ranges = []
clustersx = []
clustersy = []

data = open("dataset.txt")
line_index = 0
rng = default_rng()
random_lines = rng.choice(N, size=N, replace=False)

def euclid_distance(p1, p2):
    return distance.euclidean(p1,p2)



#compute clunion of close clusters
def merging_stage(di):
    global clustersx
    global clustersy
    #global ranges
    
    #merge clusters based on distance
    temp_clustx = list(clustersx)
    temp_clusty = list(clustersy)
    #temp_ranges = list(ranges)
    
    #remove every old center from lists
    clustersx = []
    clustersy = []
    #ranges = []
    
    #while that list is not empty
    while temp_clustx:
        num = len(temp_clustx)
        index = random.randint(0,num-1)
        
        #we are considering the indexed cluster
        centerx = temp_clustx.pop(index)
        centery = temp_clusty.pop(index)
        #rng = temp_ranges.pop(index)
        
        
        #ranges.append(rng)
        
        temp2_clustx = list(temp_clustx)
        temp2_clusty = list(temp_clusty)
        #temp2_ranges = list(temp_ranges)
        
        n = len(temp2_clustx)
        #find close centers
        for i in range(0, n):
            #check distance from indexed center to all other centers and remove the close ones
            dist = euclid_distance((centerx,centery),(temp2_clustx[i],temp2_clusty[i]))
            
            if  dist < di:
                #this center is too close, its cluster is merged
                temp_clustx.remove(temp2_clustx[i])
                temp_clusty.remove(temp2_clusty[i])
                #tr = temp2_ranges[i]
                #temp_ranges.remove(tr)
                """
                #recalculate the range if necessary
                tr += dist
                if rng < tr:
                    rng = tr
                    #bound on the range
                    if (rng > alpha*di):
                        rng = alpha*di
                        print("not epic")
                        """
        clustersx.append(centerx)
        clustersy.append(centery)
        #ranges.append(rng)
    
    return len(clustersx)


#add one new point
def update_stage():
    numclusters = len(clustersx)
    
    global data
    global pointsx
    global pointsy

    #generate new point
    # Get next line from file 
    line = read_line() 
  
    # if line is empty, end of file is reached 
    if not line: 
        return len(clustersx)

    #get point from data
    line = line.strip()
    point = line.split()
    
    pointx = float(point[0])
    pointy = float(point[1])

    pointsx.append(pointx)
    pointsy.append(pointy)

    check = 1

    #compare distance with every cluster center
    for i in range(0,numclusters):
        if euclid_distance((pointx,pointy),(clustersx[i],clustersy[i])) < d*alpha:#ranges[i] :
            #the point is within some cluster
            check = 0
    
    if check == 1:
        #the point was away from all clusters, create a new cluster
        clustersx.append(pointx)
        clustersy.append(pointy)
#        ranges.append(d)
        
    return len(clustersx)

def read_line():
    global line_index
    global random_lines
    
    line = linecache.getline("dataset.txt", random_lines[line_index])
    
    if line_index < N-1:
        line_index += 1
    
    return line

#==============================================================================

count = 0
while count < k+1 : 
    count += 1
  
    # Get next line from file 
    line = read_line()
    
    # if line is empty end of file is reached 
    if not line: 
        break
    
    #get point from data
    line = line.strip()
    point = line.split()
    
    print(point)

    pointsx.append(float(point[0]))
    pointsy.append(float(point[1]))
    
plt.scatter(pointsx,pointsy)
plt.show()


for i in range(0,k+1):
    ranges.append(0)

#find minimum distance
d = 500000
#rangei = 0
#rangej = 0

for i in range(0,k+1):
    for j in range(0,k+1):
        dist = euclid_distance((pointsx[i], pointsy[i]), (pointsx[j], pointsy[j]))
        if (dist<d and i != j):
            d = dist
  #          rangei = i
 #           rangej = j
print(d)

#associate minimum range with correct cluster indexes
#ranges[rangei] = d
#ranges[rangej] = d

#for i in range(0,k+1):
#    ranges[i] = d

clustersx = list(pointsx)
clustersy = list(pointsy)

i = 0
while i<N:
    d= beta*d
    print(d)
    
    # MERGING stage
    print("MERGING STAGE")
    
    m = merging_stage(d)
    
    plt.scatter(clustersx, clustersy, color = 'red')
    plt.show()
    
    print("UPDATE STAGE")
    #accept new inputs and UPDATE
    while m<k+1 and i<N:
        m = update_stage()
        i+=1
    
    #draw points
    f, ax = plt.subplots(1)
    ax.scatter(pointsx, pointsy ,color = "blue")
    ax.scatter(clustersx, clustersy ,color = "red")
    #draw circles for each cluster
    for k in range(0, len(clustersx)):
       ax.add_artist(plt.Circle((clustersx[k],clustersy[k]), alpha*d, color='r', fill=False))

    plt.show(f)

#draw final points
f, ax = plt.subplots(1)
ax.scatter(pointsx, pointsy ,color = "blue")
ax.scatter(clustersx, clustersy ,color = "red")

plt.show(f)

data.close()