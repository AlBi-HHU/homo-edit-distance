import numpy as np



# Main dynamic programming algorithm to compute the homo-edit distance between two strings s and t.
def homoEditDistance(s, t):
    m = len(s)
    n = len(t)
    d = np.zeros(shape=(m + 1, n + 1), dtype=object)
    H = distancesToEmptyString(s)
    H.update(distancesToEmptyString(t))
    for i in range(0, len(s) + 1):
        for j in range(0, len(t) + 1):
            C = list([])
            # initialisation
            if i == 0 and j == 0:
                d[i][j] = 0
            # main body of method
            else:
                if i>0 and j>0:
                    if s[i - 1] == t[j - 1]:
                        C.append(d[i-1][j-1])

                for k in range (0,i):
                    C.append(d[k,j]+H[(s, k, i - 1)])

                for l in range (0,j):
                    C.append(d[i,l]+H[(t, l, j - 1)])

                d[i][j] = int(min(C))

    return d[m][n]



def homoEditDistanceWbacktrack(s, t):
    m = len(s)
    n = len(t)
    d = np.zeros(shape=(m + 1, n + 1), dtype=object)
    bt = np.zeros(shape=(m + 1, n + 1), dtype=object)
    H = distancesToEmptyString(s)
    H.update(distancesToEmptyString(t))
    for i in range(0, len(s) + 1):
        for j in range(0, len(t) + 1):
            C = list([])
            # initialisation
            if i == 0 and j == 0:
                d[i][j] = 0
                bt[i][j] = list([])
            # main body of method
            else:
                c = float('inf')
                if i>0 and j>0:
                    if s[i - 1] == t[j - 1]:
                        c = d[i-1][j-1]
                        C.append((i-1,j-1))

                for k in range (0,i):
                    if c > d[k,j]+H[(s, k, i - 1)]:
                        c = d[k,j]+H[(s, k, i - 1)]
                        C = list([(k,j)])
                    elif c == d[k,j]+H[(s, k, i - 1)]:
                        C.append((k,j))

                for l in range (0,j):
                    if c > d[i,l]+H[(t, l, j - 1)]:
                        c = d[i,l]+H[(t, l, j - 1)]
                        C = list([(i,l)])
                    elif c == d[i,l]+H[(t, l, j - 1)]:
                        C.append((i,l))

                d[i][j] = c
                bt[i][j] = list(C)
    sol = backtrack(bt, s, t)
    return d[m][n], sol



def backtrack(bt, s, t):
    sub = ''
    m = len(s)
    n = len(t)
    for gen in backtrackRecursive(bt, s, t, sub, m, n):
        yield gen



def backtrackRecursive(bt, s, t, sub, i, j):
    if i == 0 and j == 0:
        yield (sub[::-1])
        return
    
    for C in bt[i][j]:
        # horizontal
        if C[0] == i:
            for gen in backtrackRecursive(bt, s, t, sub, i, C[1]):
                yield gen
        
        # vertical
        elif C[1] == j:
            for gen in backtrackRecursive(bt, s, t, sub, C[0], j):
                yield gen
            
        # diagonal
        else:
            for gen in backtrackRecursive(bt, s, t, sub + s[i - 1], C[0], C[1]):
                yield gen



# Auxiliary dynamic programming algorithm to compute the homo-edit distance between every substring of a string s and the empty string.
def distancesToEmptyString(s):
    n = len(s)
    H = dict({})

    for l in range(0, n):
        for i in range(0,n - l):
            j = i + l
            if i == j:
                H[(s, i, j)] = 1
            else:
                C = list([])
                for k in range(i, j):
                    C.append(H[(s, i, k)] + H[(s, k + 1, j)] - int(bool(s[i] == s[j])))
                H[(s, i, j)] = int(min(C))
    return H



def main():
    s = input("Please enter string s: ")
    t = input("Please enter string t: ")
    bt = input("If you want to get all subsequences of s and type in \"y\" :")
    print("The homo-edit-distance for \ts = ",end='')
    print(s,end='\t')
    print(" and \tt = ",end='')
    print(t,end='\t')
    print(" is: ",end='')
    if bt == "y":
        inst = homoEditDistanceWbacktrack(s, t)
        print(inst[0])
        for sup in set(inst[1]):
            print("\n SOLUTION:")
            print(sup)
    else:
        print(homoEditDistance(s,t))



main()