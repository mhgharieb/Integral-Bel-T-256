#! /usr/bin/#!/usr/bin/env python

from gurobipy import *

import time

from helpFunction import *

blocksize = 128

if (len(sys.argv) != 3):
    exit()

Round = int(sys.argv[1])
inputDP = sys.argv[2]

activebits = inputDP.count('1')

filename_model = "Bel-T_" + str(Round) + "_" + str(activebits) + ".lp"



# Reduced number inqualities for Bel-T S-Box
S_T = [[1, 1, 1, 36, 1, 1, 1, 1, -6, -6, -6, -6, -6, -6, -6, -6, 5],
    [1, 1, 39, 1, 1, 1, 1, 1, -7, -7, -7, -7, -6, -6, -6, -6, 6],
    [2, 68, 2, 2, 2, 2, 2, 2, -11, -11, -12, -12, -12, -11, -12, -11, 10],
    [1, 1, 1, 1, 1, 1, 35, 1, -6, -6, -6, -6, -6, -6, -6, -5, 5],
    [14, 0, 0, 0, 0, 0, 0, 0, -1, -1, -3, -3, -3, -2, -3, -1, 3],
    [0, 0, 0, 0, 9, 0, 0, 0, -2, -2, -1, 0, -2, -1, -2, -1, 2],
    [-6, -2, 0, 0, -5, 2, 2, 1, -7, -6, -6, -6, 30, -5, -7, -5, 20],
    [-8, -12, -6, -11, -8, -6, -13, -2, -6, -10, -5, -5, -12, -2, 32, 4, 70],
    [-1, -2, -2, -3, -2, -2, -2, -4, 16, 16, 17, 17, 17, 14, 17, 15, 0],
    [0, -1, -2, 0, 0, 1, 0, 0, -2, 2, 5, -3, -3, -2, -3, 2, 6],
    [1, 1, -1, 2, 0, 2, 0, 2, -1, -6, -7, 19, 1, -7, -7, -7, 8],
    [-9, -1, 0, -1, -1, 3, 3, -2, -7, -7, -6, -7, -2, 29, -5, -8, 21],
    [0, -3, -1, -1, -3, -1, 0, 2, -4, 10, -4, -3, -1, -1, 2, -5, 13],
    [-2, -1, -8, -2, -5, -5, -8, -12, 10, -15, 3, 3, -11, 3, 4, -7, 53],
    [-23, -24, -23, -21, -21, -23, -22, -26, 4, 5, 2, 3, 4, -1, 4, 4, 158],
    [-2, -4, 0, -5, -2, -1, -6, -1, -4, -4, -4, -5, -6, 3, 14, 2, 25],
    [-10, 1, 3, 2, 2, 0, 3, 3, -13, -12, -13, 47, 0, -12, -12, -12, 23],
    [-1, -2, 0, -2, -2, -1, 0, -2, 3, 3, 3, 3, 2, 3, 3, 1, 7],
    [-6, -3, -5, -7, -6, -6, -6, -4, 4, 3, 4, 5, 5, 4, 2, 1, 35],
    [-1, -2, -3, -2, 0, -1, -3, -3, 15, 15, 14, 14, 15, 12, 15, 13, 0],
    [-9, 3, -9, -9, 0, 1, -9, -9, -2, -2, 8, -3, -2, 8, -2, -12, 48],
    [-1, -1, -3, 0, 0, -1, -1, -1, -2, 1, 3, -4, -3, -2, -2, 6, 11],
    [-2, -2, 0, -2, -2, 3, -2, -2, -1, -1, -1, -1, 2, -3, -1, 2, 13],
    [-1, -2, -1, 0, -1, -1, -1, 1, -2, -3, 0, 0, -2, 0, 3, 1, 9],
    [0, 0, -1, -1, -1, -1, -1, -1, -3, 3, 1, -2, -1, 1, 1, -2, 8],
    [-1, -1, 0, -1, 0, -1, -1, -1, 0, 0, 0, -1, 0, 1, 0, 0, 6],
    [-1, -1, 0, -1, -1, -1, -1, 1, 0, 0, 0, 0, 1, 0, -1, 0, 6],
    [-2, -1, -2, -2, -2, -2, 0, -2, 2, 2, 0, 2, 2, 1, 2, 1, 11]]


def ConstraintsBySbox(X, Y):

    V = X + Y

    constraints = []
    for inq in S_T:
    	tmp = [str(a) + ' ' + str(b) for (a, b) in zip(inq[:-1], V)]
    	tmp1 = ' + '.join(tmp)
    	tmp2 = tmp1.replace("+ -", "- ")
    	tmp2 += ' >= '
    	tmp2 += str(-1 * inq[-1])
    	constraints.append(tmp2)

    return constraints



def ConstraintsByGbox(X, Y, r):
    Sbox_blockSize = 8

    # Y = Y_beforeShift <<< r
    Y_beforeShift = RotateRight(Y, r)

    #X = u1_in || u2_in || u3_in || u4_in
    u1_in = X[: Sbox_blockSize]
    u2_in = X[Sbox_blockSize : 2 * Sbox_blockSize]
    u3_in = X[2 * Sbox_blockSize : 3 * Sbox_blockSize]
    u4_in = X[3 * Sbox_blockSize:]

    #Y_beforeShift = u1_out || u2_out || u3_out || u4_out
    u1_out = Y_beforeShift[: Sbox_blockSize]
    u2_out = Y_beforeShift[Sbox_blockSize : 2 * Sbox_blockSize]
    u3_out = Y_beforeShift[2 * Sbox_blockSize : 3 * Sbox_blockSize]
    u4_out = Y_beforeShift[3 * Sbox_blockSize:]

    return ConstraintsBySbox(u1_in, u1_out) + ConstraintsBySbox(u2_in, u2_out) + ConstraintsBySbox(u3_in, u3_out) + ConstraintsBySbox(u4_in, u4_out)



def SolveModel(objective):
    time_start = time.time()
    m = read(filename_model)
    m.setParam('OutputFlag', False)
    counter = 0
    set_zero = []
    global_flag = False
    while counter < blocksize:
        m.optimize()
        # Gurobi syntax: m.Status == 2 represents the model is feasible.
        if m.Status == 2:
            obj = m.getObjective()
            if obj.getValue() > 1:
                global_flag = True
                break
            else:
                for i in range(0, blocksize):
                    u = obj.getVar(i)
                    temp = u.getAttr('x')
                    if temp == 1:
                        set_zero.append(u.getAttr('VarName'))
                        u.ub = 0
                        m.update()
                        counter += 1
                        break
        # Gurobi syntax: m.Status == 3 represents the model is infeasible.
        elif m.Status == 3:
            global_flag = True
            break
        else:
            print "Unknown error!"

    if global_flag:
        print "Integral Distinguisher Found!\n"
        
        balanceBits = []
        for i in xrange(len(objective)):
            if objective[i] not in set_zero:
                balanceBits.append(i)
        print '# of rounds: %i' %Round + " , activebits:%i " %activebits + ", Input DP: " + inputDP
        print "balanced bits: " + str(len(balanceBits)) + ' ' + str(balanceBits)      
    else:
        print "Integral Distinguisher do NOT exist\n"

    time_end = time.time()
    print("Time used = " + str(time_end - time_start) + " Seconds")


def BelTRound(r):

    variables = []
    constraints = []

    #Add Sub modulo track
    AddSubTrack = 100 * r

    branchsize = blocksize/4

    #generate Input
    Xin = CreateVariables('x', r, blocksize)
    variables += Xin

    #branches
    Ain = Xin[: branchsize]
    Bin = Xin[branchsize : 2 * branchsize]
    Cin = Xin[2 * branchsize : 3 * branchsize]
    Din = Xin[3 * branchsize:]

    #generate output
    Xout = CreateVariables('x', r+1, blocksize)

    #branches
    Aout = Xout[: branchsize]
    Bout = Xout[branchsize : 2 * branchsize]
    Cout = Xout[2 * branchsize : 3 * branchsize]
    Dout = Xout[3 * branchsize:]

    #generate auxiliary variables
    a1 = CreateVariables('a1', r, branchsize)
    a2 = CreateVariables('a2', r, branchsize)
    variables += a1 + a2

    b1 = CreateVariables('b1', r, branchsize)
    b2 = CreateVariables('b2', r, branchsize)
    b3 = CreateVariables('b3', r, branchsize)
    variables += b1 + b2 + b3

    c1 = CreateVariables('c1', r, branchsize)
    c2 = CreateVariables('c2', r, branchsize)
    c3 = CreateVariables('c3', r, branchsize)
    c4 = CreateVariables('c4', r, branchsize)
    variables += c1 + c2 + c3 + c4

    d1 = CreateVariables('d1', r, branchsize)
    d2 = CreateVariables('d2', r, branchsize)
    variables += d1 + d2

    ab1 = CreateVariables('ab1', r, branchsize)
    ab2 = CreateVariables('ab2', r, branchsize)
    ab3 = CreateVariables('ab3', r, branchsize)
    ab4 = CreateVariables('ab4', r, branchsize)
    ab5 = CreateVariables('ab5', r, branchsize)
    ab6 = CreateVariables('ab6', r, branchsize)
    ab7 = CreateVariables('ab7', r, branchsize)
    ab8 = CreateVariables('ab8', r, branchsize)
    ab9 = CreateVariables('ab9', r, branchsize)
    variables += ab1 + ab2 + ab3 + ab4 + ab5 + ab6 + ab7 + ab8 + ab9

    cd1 = CreateVariables('cd1', r, branchsize)
    cd2 = CreateVariables('cd2', r, branchsize)
    cd3 = CreateVariables('cd3', r, branchsize)
    cd4 = CreateVariables('cd4', r, branchsize)
    cd5 = CreateVariables('cd5', r, branchsize)
    cd6 = CreateVariables('cd6', r, branchsize)
    cd7 = CreateVariables('cd7', r, branchsize)
    cd8 = CreateVariables('cd8', r, branchsize)
    cd9 = CreateVariables('cd9', r, branchsize)
    variables += cd1 + cd2 + cd3 + cd4 + cd5 + cd6 + cd7 + cd8 + cd9

    bc1 = CreateVariables('bc1', r, branchsize)
    bc2 = CreateVariables('bc2', r, branchsize)
    bc3 = CreateVariables('bc3', r, branchsize)
    bc4 = CreateVariables('bc4', r, branchsize)
    bc5 = CreateVariables('bc5', r, branchsize)
    bc6 = CreateVariables('bc6', r, branchsize)
    bc7 = CreateVariables('bc7', r, branchsize)
    variables += bc1 + bc2 + bc3 + bc4 + bc5 + bc6 + bc7


    #branch a
    constraints += Copylist(Ain, [a1, ab1])

    addVariables, addConstraints = ConstraintsByModSubVariables(a1, ab6, a2, AddSubTrack)
    AddSubTrack +=1
    variables += addVariables
    constraints += addConstraints

    constraints += Copylist(a2, [ab7, Cout])

    #branch b
    constraints += XORlist([Bin, ab3], b1)

    constraints += Copylist(b1, [b2, ab4, bc1])

    addVariables, addConstraints = ConstraintsByModAddVariables(b2, bc7, b3, AddSubTrack)
    AddSubTrack +=1
    variables += addVariables
    constraints += addConstraints

    constraints += XORlist([b3, ab9], Aout)

    #branch c
    constraints += XORlist([Cin, cd3], c1)

    constraints += Copylist(c1, [bc2, c2])

    addVariables, addConstraints = ConstraintsByModSubVariables(c2, bc6, c3, AddSubTrack)
    AddSubTrack +=1
    variables += addVariables
    constraints += addConstraints

    constraints += Copylist(c3, [cd4, c4])

    constraints += XORlist([c4, cd9], Dout)

    #branch d
    constraints += Copylist(Din, [d1, cd1])

    addVariables, addConstraints = ConstraintsByModAddVariables(d1, cd6, d2, AddSubTrack)
    AddSubTrack +=1
    variables += addVariables
    constraints += addConstraints

    constraints += Copylist(d2, [cd7, Bout])

    #ab
    addVariables, addConstraints = ConstraintsByModAddConstant(ab1, ab2, AddSubTrack)
    AddSubTrack +=1
    variables += addVariables
    constraints += addConstraints

    constraints += ConstraintsByGbox(ab2, ab3, 5)

    addVariables, addConstraints = ConstraintsByModAddConstant(ab4, ab5, AddSubTrack)
    AddSubTrack +=1
    variables += addVariables
    constraints += addConstraints

    constraints += ConstraintsByGbox(ab5, ab6, 13)

    addVariables, addConstraints = ConstraintsByModAddConstant(ab7, ab8, AddSubTrack)
    AddSubTrack +=1
    variables += addVariables
    constraints += addConstraints

    constraints += ConstraintsByGbox(ab8, ab9, 21)

    #cd
    addVariables, addConstraints = ConstraintsByModAddConstant(cd1, cd2, AddSubTrack)
    AddSubTrack +=1
    variables += addVariables
    constraints += addConstraints

    constraints += ConstraintsByGbox(cd2, cd3, 21)

    addVariables, addConstraints = ConstraintsByModAddConstant(cd4, cd5, AddSubTrack)
    AddSubTrack +=1
    variables += addVariables
    constraints += addConstraints

    constraints += ConstraintsByGbox(cd5, cd6, 13)

    addVariables, addConstraints = ConstraintsByModAddConstant(cd7, cd8, AddSubTrack)
    AddSubTrack +=1
    variables += addVariables
    constraints += addConstraints

    constraints += ConstraintsByGbox(cd8, cd9, 5)

    #bc
    addVariables, addConstraints = ConstraintsByModAddVariables(bc1, bc2, bc3, AddSubTrack)
    AddSubTrack +=1
    variables += addVariables
    constraints += addConstraints

    addVariables, addConstraints = ConstraintsByModAddConstant(bc3, bc4, AddSubTrack)
    AddSubTrack +=1
    variables += addVariables
    constraints += addConstraints

    constraints += ConstraintsByGbox(bc4, bc5, 21)

    constraints += Copylist(bc5, [bc6, bc7])

    return (variables, constraints)



def WriteModel(constraints, variables, objective):
    file_co = open(filename_model, 'w+')
    file_co.write('Minimize\n')
    file_co.write(' + '.join(objective) + '\n')
    file_co.write('Subject To\n')
    for enq in constraints:
    	file_co.write(enq + '\n')
    file_co.write('Binary\n')
    for v in variables:
    	file_co.write(v + '\n')
    file_co.close()

def main():
    variables = []
    constraints = []
    for r in xrange(Round):
        if r == 0:
            Xin = CreateVariables('x', r, blocksize)
            for i in xrange(blocksize):
            	constraints.append(Xin[i] + ' = ' + inputDP[i])

        roundVariable , roundConstraints = BelTRound(r)
        variables += roundVariable
        constraints += roundConstraints

        if r == Round - 1:
            Xout = CreateVariables('x', r+1, blocksize)
            variables += Xout
            objective = Xout

    WriteModel(constraints, variables, objective)
    SolveModel(objective)

main()
