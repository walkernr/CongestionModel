# -*- coding: utf-8 -*-
"""
Created on Sun Feb 09 17:23:47 2014

@author: Redacted
"""

import numpy as np
import random as r
import matplotlib.pyplot as plt

#initial values
d = 100 #length of freeway segment
t = 100 #timsteps to be calculated
pc = .15 #probability of car spawning
ps = .05 #probability of slowdown
s = 7 #maximum velocity
param = '\n' + '$p_{spawn}$ = ' + str(pc) + '\t' + '$p_{slow}$ = ' + str(ps) + '\t' + '$v_{max}$ = ' + str(s) #header for the plot according to initial data

def addScatter(a, b):
    """plots a line of points as car positions, takes in array and timestep"""
    colors = ['red', 'blue'] #red is the left lane, blue is the right lane
    c = [] #a list of the count of cars in each lane
    v = [] #a list of all of the velocities of the cars

    for n in range(2): #loop through both lanes
        x = [] #x values in the scatterplot (location of the car on the freeway)
        y = [] #y values of the scatterplot (the time)

        for i in range(len(a[n])): #loop through every index in the lane
            if a[n][i] > -1: #if a car exists at the index
                x.append(i) #append the index of the car for the scatterplot
                v.append(a[n][i]) #append the velocity of the car at the index
                y.append((-1) ** n * b + (-1) ** n) #append the time, left lane plots up in time, right lane plots down in time
        c.append(len(x)) #append the number of cars in the lane
        plt.subplot(211) #first subplot (scatterplot of cars)
        plt.scatter(x, y, color = colors[n], s = 20, marker = 's') #plot the car positions at the time, marked by squares

    va = float(sum(v)) / float(len(v)) #average velocity for all cars
    print str(b) + '\t' + str(sum(v)) + '\t' + str(len(v)) #print the timestep, total velocity, and total cars
    plt.subplot(212) #second subplot (velocity and ratio of cars in the left and right lanes)
    plt.scatter(b, va, color = colors[0], s = 20, marker = '4') #plot the average velocity, denoted by rightward triangle
    plt.scatter(b, float(c[0]) / float(c[1]), color = colors[1], s = 20, marker = '_') #plot the ratio, denoted by a _
    return v #return the list of velocities

def accelAll(a):
    """accelerates all cars in the given two dimensional array"""

    for n in range(2): #loop through both lanes
        for i in range(len(a[n])): #loop through each indes in each lane
            if a[n][i] > -1 and a[n][i] < s: #if a car exists there, and is travelling below the speed limit
                a[n][i] += 1 #accelerate the car

    return a #return the list of accelerated cars

def switchLane(a, c):
    """determines whether cars in the given two dimensional array should switch lanes, given the case"""
    #IS B NECESSARY?
    b = -1 * np.ones((2, len(a[0])), dtype = int) #initialize a copy of the list of cars

    for n in range(2): #loop through each lane
        for i in range(len(a[n])): #loop through each index in the lane
            b[n][i] = a[n][i] #copy data over to the copy from the list

    for n in range(2): #loop through the two lanes

        if c == 2 and n == 0: #if we are in the conventional case and the left lane
            for i in range(len(a[0])): #loop through cars

                if a[0][i] > -1 and a[1][i] < 0: #if the car exists at the index and the adjacent space is empty
                    s = True #we assume it will pass
                    v = a[0][i] #store the velocity of a

                    for j in range(i + 1, min(i + v + 1, len(a[0]))): #loop through the space in front of the car in the other lane
                        if b[1][j] > -1: #if the space in the other lane has a car
                            s = False #it does not pass in order to retain velocity

                    if i + v >= len(a[0]): #if the car is going fast enough such that it loops around to the start

                        for k in range((i + v) % (len(a[n]) - 1)): #loop through the cars in the other lane within range of the car
                            if b[1][k] > -1: #if the space is filled
                                s = False #it does not pass in order to retain velocity

                    if s == True: #if passing is preferred
                        for j in range(i): #loop through spaces behind car
                            if j + b[1][j] >= i: #if the cars behind the car in the other lane are going fast enough to meet its position
                                s = False #passing is not preferred in order to avoid slowing cars in the slow lane

                    if s == True: #if passing is preferred
                        a[0][i] = -1 #the current position is emptied
                        a[1][i] = v #the adjacent position is the new position of the car

        else:
            for i in range(len(a[n])):

                if a[n][i] > -1:
                    s = False
                    v = a[n][i]

                    if i + v < len(a[n]):
                        for j in range(i + 1, i + v + 1):
                            if b[n][j] > -1 and s == False:
                                if i + v >= j and a[(n + 1) % 2][i] < 0 and r.uniform(0, 1) <= 1 - float((j - i - 1) / v) - .25:
                                    if b[(n + 1) % 2][j] < 0:
                                        a[(n + 1) % 2][i] = v + 1
                                        a[n][i] = -1
                                        s = True
                        if s == True:
                            for k in range(i):
                                if k + a[(n + 1) % 2][k] >= i:
                                    a[(n + 1) % 2][i] = -1
                                    a[n][i] = v
                                    s = False

                    if i + v >= len(a[n]):

                        for j in range(i + 1, len(a[n])):
                            if b[n][j] > -1 and s == False:
                                if i + v >= j and a[(n + 1) % 2][i] < 0 and r.uniform(0, 1) <= 1 - float((j - i - 1) / v) - .25:
                                    if b[(n + 1) % 2][j] < 0:
                                        a[(n + 1) % 2][i] = v + 1
                                        a[n][i] = -1
                                        s = True

                        for k in range((i + v) % (len(a[n]) - 1)):
                            if b[n][k] > -1 and s == False:
                                if (i + v) % len(a[n]) >= k:
                                    if i + v >= j and a[(n + 1) % 2][i] < 0 and r.uniform(0, 1) <= 1 - float(((len(a[n]) - i) + k - 1) / v) - .25:
                                        if b[(n + 1) % 2][j] < 0:
                                            a[(n + 1) % 2][i] = v + 1
                                            a[n][i] = -1
                                            s = True
                        if s == True:
                            for l in range(i):
                                if l + a[(n + 1) % 2][l] >= i:
                                    a[(n + 1) % 2][i] = -1
                                    a[n][i] = v
                                    s = False
    return a

def avoidCollide(a):
    """modifies velocities to avoid collisions given an array of cars"""
    b = -1 * np.ones((2, len(a[0])), dtype = int) #initialize copy of a

    for n in range(2): #loop through lanes

        for i in range(len(a[n])): #iterate through positions
            b[n][i] = a[n][i] #copy value over

    for n in range(2): #loop through lanes

        for i in range(len(a[n])): #loop through positions
            if a[n][i] > -1: #if the position is occupied
                c = False #there is no collision by default
                v = a[n][i] #store velocity

                for j in range(i + 1, min(i + v + 1, len(a[n]))): #check from current position to end of travel or end of list
                    if b[n][j] > -1 and c == False: #if the space is occupied and there is no recorded collision
                        a[n][i] = j - i - 1 #the car is slowed to avoid collision
                        c = True #a collision has been recorded and avoided

                if i + v >= len(a[n]): #if the car has a velocity such that it loops around to the front

                    for k in range((i + v) % (len(a[n]) - 1)): #check positions behind the projected position
                        if b[n][k] > -1 and c == False: #if a car exists at the position and there is no recorded collision
                            a[n][i] = (len(a[n]) - i) + k - 1 #the car is slowed to avoid collision
                            c = True #a collision has been logged and avoided
    return a

def randSlow(a, b):
    """performs random slowdowns on cars to promote traffic conjestions by taking in an array of cars"""

    for n in range(2): #loop through lanes
        for i in range(len(a[n])): #loop through positions in lane
            if a[n][i] > 0: #if car exists at position
                if r.uniform(0, 1) <= b: #there is only a probability of slowdown
                    a[n][i] -= 1 #perform slowdown

    return a

def stepForward(a):
    b = -1 * np.ones((2, len(a[0])), dtype = int)

    for n in range(2):
        for i in range(len(a[n])):
            if a[n][i] > -1:
                v = a[n][i]
                b[n][(i + v) % len(a[n])] = v

    return b

def generateCars(a, b, c):

    for i in range(len(a)):
        if r.uniform(0, 1) <= b:
            a[i] = r.choice(range(c / 2, c + 1))

    return a

c = -1 * np.ones((2, d), dtype = int)

#c[0] = generateCars(c[0], pc, s)
c[1] = generateCars(c[1], pc, s)

for n in range(3):
    va = 0.
    vl = 0.
    cc = -1 * np.ones((2, d), dtype = int)

    for i in range(2):
        for j in range(len(c[i])):
            cc[i][j] = c[i][j]

    plt.clf()

    fig = plt.figure(dpi = 120, figsize = (16.0, 9.0))
    plt.subplots_adjust(hspace = .3, top = .85)

    ax1 = fig.add_subplot(211)
    ax1.set_title('Density Map')
    ax1.set_xlabel('Position')
    ax1.set_ylabel('Time')
    ax1.set_xlim(0, d)
    ax1.set_ylim(-t, t)

    ax2 = fig.add_subplot(212)
    ax2.set_title('Velocity and Lane Density Ratio')
    ax2.set_xlabel('Time')
    ax2.set_ylabel('Velocity or Cl/Cr')
    ax2.set_xlim(0, d)
    ax2.set_ylim(0, s)

    for i in range(t):
        v = addScatter(cc, i)
        va += sum(v)
        vl += len(v)
        cc = accelAll(cc)
        if n == 1 or n == 2:
            cc = switchLane(cc, n)
        cc = avoidCollide(cc)
        cc = randSlow(cc, ps)
        cc = stepForward(cc)

    vta = r'$\bar{v}$ = ' + str(va/vl)
    tn = r'total cars = ' + str(len(v))
    ax2.text(.25 * d, s + .1, tn, fontsize = 10)
    ax2.text(.65 * d, s + .1, vta, fontsize = 10)

    if n == 0:
        plt.suptitle('Two Lanes With No Passing ' + param, fontsize = 20)
        plt.savefig(str(pc) + '-' + str(ps) + '-' + str(s) + '-2LNP' + '.png')

    if n == 1:
        plt.suptitle('Two Lanes With Free Passing' + param, fontsize = 20)
        plt.savefig(str(pc) + '-' + str(ps) + '-' + str(s) + '-2LFP' + '.png')

    if n == 2:
        plt.suptitle('Two Lanes With Contemporary Passing Convention' + param, fontsize = 20)
        plt.savefig(str(pc) + '-' + str(ps) + '-' + str(s) + '-2LCP' + '.png')