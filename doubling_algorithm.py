
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

input_path = "dataset.txt" #path of input file
N = 5000 # number of input points
k = 15  #number of clusters
alpha = 2
beta = 2

#lists of all points read from input file
pointsx = []
pointsy = []

#lists of cluster centers coordinates
clustersx = []
clustersy = []

#give a random order to the input every time the program is run
line_index = 0
rng = default_rng()
random_lines = rng.choice(N, size=N, replace=False)



def euclid_distance(p1, p2):
    return distance.euclidean(p1,p2)



#union of close clusters
def merging_stage(di):
    global clustersx
    global clustersy
    
    #last phase centers
    temp_clustx = list(clustersx)
    temp_clusty = list(clustersy)
    
    #remove every old center from lists
    clustersx = []
    clustersy = []
    
    #while that list is not empty aka we considered every center
    while temp_clustx:
        num = len(temp_clustx)
        index = random.randint(0,num-1)
        
        #we are considering the indexed cluster
        centerx = temp_clustx.pop(index)
        centery = temp_clusty.pop(index)
        
        #save all other centers to make comparison with indexed center easier
        temp2_clustx = list(temp_clustx)
        temp2_clusty = list(temp_clusty)
        
        n = len(temp2_clustx)
        #find close centers
        for i in range(0, n):
            #check distance from indexed center to all other centers and remove the close ones
            dist = euclid_distance((centerx,centery),(temp2_clustx[i],temp2_clusty[i]))
            
            if  dist < di:
                #this center is too close, its cluster is merged
                temp_clustx.remove(temp2_clustx[i])
                temp_clusty.remove(temp2_clusty[i])

        clustersx.append(centerx)
        clustersy.append(centery)
    
    return len(clustersx)



#add one new point
def update_stage():
    numclusters = len(clustersx)
    
    global data
    global pointsx
    global pointsy

    # get next point from file 
    line = read_line() 
  
    # if line is empty, end of file is reached 
    if not line: 
        return len(clustersx)

    #get point from data and separate coordinates
    line = line.strip()
    point = line.split()
    
    pointx = float(point[0])
    pointy = float(point[1])

    #add new point to list of all points
    pointsx.append(pointx)
    pointsy.append(pointy)

    check = 1

    #compare distance with every cluster center
    for i in range(0,numclusters):
        if euclid_distance((pointx,pointy),(clustersx[i],clustersy[i])) < d*alpha:#ranges[i] :
            #the point is within some cluster, nothing happens
            check = 0
    
    if check == 1:
        #the point was far enough from all clusters, create a new cluster
        clustersx.append(pointx)
        clustersy.append(pointy)
        
    return len(clustersx)



#read next random line from input file
def read_line():
    global line_index
    global random_lines
    
    line = linecache.getline(input_path, random_lines[line_index])
    
    if line_index < N-1:
        line_index += 1
    
    return line

#==============================================================================


#--------------------------------------------------INITIALIZATION
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

#find minimum distance
d = 5000000
for i in range(0,k+1):
    for j in range(0,k+1):
        dist = euclid_distance((pointsx[i], pointsy[i]), (pointsx[j], pointsy[j]))
        if (dist<d and i != j):
            d = dist
            
print(d)

#initilaise cluster centers lists
clustersx = list(pointsx)
clustersy = list(pointsy)


i = 0

#start collecting new points

while i<N:
    #update d
    d= beta*d
    print(d)
    
    # --------------------------------------------MERGING stage
    m = merging_stage(d)
    
    plt.scatter(clustersx, clustersy, color = 'red')
    plt.show()
    
    print("UPDATE STAGE")
    #accept new inputs and -----------------------UPDATE
    while m<k+1 and i<N:
        m = update_stage()
        i+=1
    
    #draw points and centers after end of phase
    f, ax = plt.subplots(1)
    ax.scatter(pointsx, pointsy ,color = "blue")
    ax.scatter(clustersx, clustersy ,color = "red")
    #draw circles for each cluster
    for k in range(0, len(clustersx)):
       ax.add_artist(plt.Circle((clustersx[k],clustersy[k]), alpha*d, color='r', fill=False))

    plt.show(f)

#draw final points and centers
f, ax = plt.subplots(1)
ax.scatter(pointsx, pointsy ,color = "blue")
ax.scatter(clustersx, clustersy ,color = "red")

plt.show(f)