

def CopyVariable(x, l):
    return [x + '_%02i' %i for i in xrange(l)]

def Copy(a, B):
    #(a) --COpy--> (b0, b1, ... , bm)
    return [a + ' - ' + ' - '.join(B) + ' = 0']

def XOR(A, b):
    #(a0, a1, ... , am) --XOR--> (b)
    return [' + '.join(A) + ' - ' + b + ' = 0']

def AND(A, b):
    #(a0, a1) --AND--> (b)
    return [
    b + ' - ' + A[0] + ' >= 0',
    b + ' - ' + A[1] + ' >= 0',
    b + ' - ' + A[0] + ' - ' + A[1] + ' <= 0'
    ]


def CreateVariables(x, Track, l):
    return [x + '_%03i' %Track + '_%03i' %i for i in xrange(l)]

def XORlist(AB, C):
    #(A, ... , B) --XOR--> (C)
    #([[a0, a1, ... , am], ... ,[b0, b1, ... , bm]]) --XOR--> ([c0, c1, ... , cm])
    #(a0, b0) --XOR--> (c0) , (a1, b1) --XOR--> (c1), ... , (am, bm) --XOR--> (cm)

    constraints = []
    #[[a0, a1, ... , am], ... ,[b0, b1, ... , bm]] ==> [[a0, ... , b0], [a1, ... , b1], ... , [am, ... ,  bm]]
    AB_Transpose = map(list, zip(*AB))
    for i in xrange(len(C)):
        constraints += XOR(AB_Transpose[i], C[i])
    return constraints

def RotateLeft(X, m):
    return X[m:] + X[:m]

def RotateRight(X, m):
    return X[-1*m:] + X[:-1*m]


def Copylist(A, BC):
    #(A) --Copy--> (B, ... , C)
    #([a0, a1, ... , am]) --Copy--> ([[b0, b1, ... , bm], ... , [c0, c1, ... , cm]])
    #(a0) --Copy--> (b0, ... , c0) , (a1) --Copy--> (b1, ... , c1), ... , (am) --Copy--> (bm, ... , cm)

    constraints = []
    #[[b0, b1, ... , bm], ... , [c0, c1, ... , cm]] ==> [[b0, ... , c0], [b1, ... , c1], ... [bm, ... , cm]]
    BC_Transpose = map(list, zip(*BC))
    for i in xrange(len(A)):
        constraints += Copy(A[i], BC_Transpose[i])
    return constraints


def ConstraintsByModAddVariables(X, Y, Z, addTrack):
    # Z = X + Y

    assert((len(X) == len(Y)) & (len(X) == len(Z)))
    Variables = []
    Constraints = []
    n = len(X)
    #auxiliary variables
    v = CreateVariables('vA', addTrack, n-1)
    m = CreateVariables('mA', addTrack, n-2)
    g = CreateVariables('gA', addTrack, n-2)
    r = CreateVariables('rA', addTrack, n-2)
    q = CreateVariables('qA', addTrack, n-2)
    w = CreateVariables('wA', addTrack, n-2)

    Variables += v + m + g + r + q + w

    #1. (a_n-1) --Copy--> (a_n-1_0, a_n-1_1)
    [a0, a1] = CopyVariable(X[n-1], 2)
    Variables += [a0, a1]
    Constraints += Copy(X[n-1], [a0, a1])

    #2. (b_n-1) --Copy--> (b_n-1_0, b_n-1_1)
    [b0, b1] = CopyVariable(Y[n-1], 2)
    Variables += [b0, b1]
    Constraints += Copy(Y[n-1], [b0, b1])

    #3. (a_n-1_0, b_n-1_0) --XOR--> (d_n-1)
    Constraints += XOR([a0, b0], Z[n-1])

    #4. (a_n-1_1, b_n-1_1) --AND--> (v0)
    Constraints += AND([a1, b1], v[0])

    #5. (v0) --Copy--> (g0, r0)
    Constraints += Copy(v[0], [g[0], r[0]])

    #6. (a_n-2) --Copy--> (a_n-2_0, a_n-2_1, a_n-2_2)
    [a0, a1, a2] = CopyVariable(X[n-2], 3)
    Variables += [a0, a1, a2]
    Constraints += Copy(X[n-2], [a0, a1, a2])

    #7. (b_n-2) --Copy--> (b_n-2_0, b_n-2_1, b_n-2_2)
    [b0, b1, b2] = CopyVariable(Y[n-2], 3)
    Variables += [b0, b1, b2]
    Constraints += Copy(Y[n-2], [b0, b1, b2])

    for i in xrange(2, n-1):
        #8. (a_n-i_0, b_n-i_0, g_i-2) --XOR--> (d_n-i)
        Constraints += XOR([a0, b0, g[i-2]], Z[n-i])

        #9. (a_n-i_1, b_n-i_1) --AND--> (v_i-1)
        Constraints += AND([a1, b1], v[i-1])

        #10. (a_n-i_2, b_n-i_2) --XOR--> (m_i-2)
        Constraints += XOR([a2, b2], m[i-2])

        #11. (m_i-2, r_i-2) --AND--> (q_i-2)
        Constraints += AND([m[i-2], r[i-2]], q[i-2])

        #12. (v_i-1, q_i-2) --XOR--> (w_i-2)
        Constraints += XOR([v[i-1], q[i-2]], w[i-2])

        #13. (w_i-2) --Copy--> (g_i-1, r_i-1)
        Constraints += Copy(w[i-2], [g[i-1], r[i-1]])

        #14. (a_n-i-1) --Copy--> (a_n-i-1_0, a_n-i-1_1, a_n-i-1_2)
        [a0, a1, a2] = CopyVariable(X[n-i-1], 3)
        Variables += [a0, a1, a2]
        Constraints += Copy(X[n-i-1], [a0, a1, a2])

        #15. (b_n-i-1) --Copy--> (b_n-i-1_0, b_n-i-1_1, b_n-i-1_2)
        [b0, b1, b2] = CopyVariable(Y[n-i-1], 3)
        Variables += [b0, b1, b2]
        Constraints += Copy(Y[n-i-1], [b0, b1, b2])

    #16. (a_1_0, b_1_0, g_n-3) --XOR--> (d_1)
    Constraints += XOR([a0, b0, g[n-3]], Z[1])

    #17. (a_1_1, b_1_1) --AND--> (v_n-2)
    Constraints += AND([a1, b1], v[n-2])

    #18. (a_1_2, b_1_2) --XOR--> (m_n-3)
    Constraints += XOR([a2, b2], m[n-3])

    #19. (m_n-3, r_n-3) --AND--> (q_n-3)
    Constraints += AND([m[n-3], r[n-3]], q[n-3])

    #20. (v_n-2, q_n-3) --XOR--> (w_n-3)
    Constraints += XOR([v[n-2], q[n-3]], w[n-3])

    #21. (a_0, b_0, w_n-3) --XOR--> (d_0)
    Constraints += XOR([X[0], Y[0], w[n-3]], Z[0])


    return (Variables, Constraints)



def ConstraintsByModSubVariables(X, Y, Z, addTrack):
    #Z = X -Y

    assert((len(X) == len(Y)) & (len(X) == len(Z)))
    Variables = []
    Constraints = []
    n = len(X)
    #auxiliary variables
    v = CreateVariables('vA', addTrack, n-1)
    m = CreateVariables('mA', addTrack, n-2)
    g = CreateVariables('gA', addTrack, n-2)
    r = CreateVariables('rA', addTrack, n-2)
    q = CreateVariables('qA', addTrack, n-2)
    w = CreateVariables('wA', addTrack, n-2)

    tmp = CreateVariables('tmpA', addTrack, 2)

    Variables += v + m + g + r + q + w + tmp

    #1. (a_n-1) --Copy--> (a_n-1_0, a_n-1_1)
    [a0, a1, a2] = CopyVariable(X[n-1], 3)
    Variables += [a0, a1, a2]
    Constraints += Copy(X[n-1], [a0, a1, a2])

    #2. (b_n-1) --Copy--> (b_n-1_0, b_n-1_1)
    [b0, b1, b2] = CopyVariable(Y[n-1], 3)
    Variables += [b0, b1, b2]
    Constraints += Copy(Y[n-1], [b0, b1, b2])

    #3. (a_n-1_0, b_n-1_0) --XOR--> (d_n-1)
    Constraints += XOR([a0, b0], Z[n-1])

    # #4. (a_n-1_1, b_n-1_1) --AND--> (v0)
    # Constraints += AND([a1, b1], v[0])
    #4.1
    Constraints += XOR([a2, b2], tmp[0])
    #4.2
    Constraints += AND([a1, b1], tmp[1])
    #4.3
    Constraints += XOR([tmp[0], tmp[1]], v[0])

    #5. (v0) --Copy--> (g0, r0)
    Constraints += Copy(v[0], [g[0], r[0]])

    #6. (a_n-2) --Copy--> (a_n-2_0, a_n-2_1, a_n-2_2)
    [a0, a1, a2] = CopyVariable(X[n-2], 3)
    Variables += [a0, a1, a2]
    Constraints += Copy(X[n-2], [a0, a1, a2])

    #7. (b_n-2) --Copy--> (b_n-2_0, b_n-2_1, b_n-2_2)
    [b0, b1, b2] = CopyVariable(Y[n-2], 3)
    Variables += [b0, b1, b2]
    Constraints += Copy(Y[n-2], [b0, b1, b2])

    for i in xrange(2, n-1):
        #8. (a_n-i_0, b_n-i_0, g_i-2) --XOR--> (d_n-i)
        Constraints += XOR([a0, b0, g[i-2]], Z[n-i])

        #9. (a_n-i_1, b_n-i_1) --AND--> (v_i-1)
        Constraints += AND([a1, b1], v[i-1])

        #10. (a_n-i_2, b_n-i_2) --XOR--> (m_i-2)
        Constraints += XOR([a2, b2], m[i-2])

        #11. (m_i-2, r_i-2) --AND--> (q_i-2)
        Constraints += AND([m[i-2], r[i-2]], q[i-2])

        #12. (v_i-1, q_i-2) --XOR--> (w_i-2)
        Constraints += XOR([v[i-1], q[i-2]], w[i-2])

        #13. (w_i-2) --Copy--> (g_i-1, r_i-1)
        Constraints += Copy(w[i-2], [g[i-1], r[i-1]])

        #14. (a_n-i-1) --Copy--> (a_n-i-1_0, a_n-i-1_1, a_n-i-1_2)
        [a0, a1, a2] = CopyVariable(X[n-i-1], 3)
        Variables += [a0, a1, a2]
        Constraints += Copy(X[n-i-1], [a0, a1, a2])

        #15. (b_n-i-1) --Copy--> (b_n-i-1_0, b_n-i-1_1, b_n-i-1_2)
        [b0, b1, b2] = CopyVariable(Y[n-i-1], 3)
        Variables += [b0, b1, b2]
        Constraints += Copy(Y[n-i-1], [b0, b1, b2])

    #16. (a_1_0, b_1_0, g_n-3) --XOR--> (d_1)
    Constraints += XOR([a0, b0, g[n-3]], Z[1])

    #17. (a_1_1, b_1_1) --AND--> (v_n-2)
    Constraints += AND([a1, b1], v[n-2])

    #18. (a_1_2, b_1_2) --XOR--> (m_n-3)
    Constraints += XOR([a2, b2], m[n-3])

    #19. (m_n-3, r_n-3) --AND--> (q_n-3)
    Constraints += AND([m[n-3], r[n-3]], q[n-3])

    #20. (v_n-2, q_n-3) --XOR--> (w_n-3)
    Constraints += XOR([v[n-2], q[n-3]], w[n-3])

    #21. (a_0, b_0, w_n-3) --XOR--> (d_0)
    Constraints += XOR([X[0], Y[0], w[n-3]], Z[0])


    return (Variables, Constraints)

def ConstraintsByModAddConstant(X, Z, addTrack):
    #Z = X + constant

    assert(len(X) == len(Z))
    Variables = []
    Constraints = []
    n = len(X)
    #auxiliary variables
    v = CreateVariables('vA', addTrack, n-2)
    g = CreateVariables('gA', addTrack, n-2)
    f = CreateVariables('fA', addTrack, n-2)
    e = CreateVariables('eA', addTrack, n-2)

    Variables += v + g + f + e

    #1. (x_n-1) --Copy--> (z_n-1,f_0, g_0)
    Constraints += Copy(X[n-1], [Z[n-1], f[0], g[0]])

    #2. (x_n-2) --Copy--> (x_n-2_0, x_n-2_1, x_n-2_2)
    [a0, a1, a2] = CopyVariable(X[n-2], 3)
    Variables += [a0, a1, a2]
    Constraints += Copy(X[n-2], [a0, a1, a2])

    #3. (x_n-2_0, f_0) --XOR--> (z_n-2)
    Constraints += XOR([a0, f[0]], Z[n-2])

    #4. (x_n-2_1, g_0) --AND--> (e_0)
    Constraints += AND([a1, g[0]], e[0])

    #5. (x_n-2_2, e_0) --XOR--> (v_0)
    Constraints += XOR([a2, e[0]], v[0])

    for i in xrange(1, n-2):

        #6. (v_i-1) --Copy--> (f_i, g_i)
        Constraints += Copy(v[i-1], [f[i], g[i]])

        #7. (x_n-2-i) --Copy--> (x_n-2-i_0, x_n-2-i_1, x_n-2-i_2)
        [a0, a1, a2] = CopyVariable(X[n-2-i], 3)
        Variables += [a0, a1, a2]
        Constraints += Copy(X[n-2-i], [a0, a1, a2])

        #8. (x_n-2-i_0, f_i) --XOR--> (z_n-2-i)
        Constraints += XOR([a0, f[i]], Z[n-2-i])

        #9. (x_n-2-i_1, g_i) --AND--> (e_i)
        Constraints += AND([a1, g[i]], e[i])

        #10. (x_n-2-i_2, e_i) --XOR--> (v_i)
        Constraints += XOR([a2, e[i]], v[i])

    #11. (x_0, v_n-3) --XOR--> (z_0)
    Constraints += XOR([X[0], v[n-3]], Z[0])


    return (Variables, Constraints)
