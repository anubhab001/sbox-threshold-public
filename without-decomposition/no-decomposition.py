# Tested in Sage 9.3



from sage.all import *


def mobious_matrix(n):

    if n == 1:
        return Matrix(GF(2), [1])
    elif n == 2:
        return Matrix(GF(2), [[1, 1], [0, 1]])
    elif n == 4:
        return Matrix(GF(2), [[1, 1, 1, 1], [0, 1, 0, 1], [0, 0, 1, 1], [0, 0, 0, 1]])
    elif n == 8:
        return Matrix(GF(2), [[1, 1, 1, 1, 1, 1, 1, 1], [0, 1, 0, 1, 0, 1, 0, 1], [0, 0, 1, 1, 0, 0, 1, 1], [0, 0, 0, 1, 0, 0, 0, 1], [0, 0, 0, 0, 1, 1, 1, 1], [0, 0, 0, 0, 0, 1, 0, 1], [0, 0, 0, 0, 0, 0, 1, 1], [0, 0, 0, 0, 0, 0, 0, 1]])
    elif n == 16:
        return Matrix(GF(2), [(1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1), (0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1), (0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1), (0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1), (0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1), (0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1), (0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1), (0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1), (0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1), (0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1), (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1), (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1), (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1), (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1), (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1), (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1)])
    else:
        M = mobious_matrix(n//2)
        return block_matrix([[M, M], [zero_matrix(GF(2), n//2), M]])


def bitslice_encoding(sbx):
    return Matrix(map(lambda x: vector(reversed(sbx.to_bits(x))), sbx)).transpose()
        

def coordinate_encoding(sbx, size=None):
    if size == None:
        size = sbx.n
    m = mobious_matrix(n=2**size)
    b = bitslice_encoding(sbx)
    
    C = b * m
    return C


def check_correctness(Y, y, logfile):
    if (sum(Y) + y) == 0: # "Correctness" is satisfied
        print ('"Correctness" satisfied', file=logfile)
        return True
    else:
        print ('"Correctness" NOT satisfied:', sum(Y)+y, file=logfile)
        return False


def check_incompleteness(Y, X, logfile):

    satisfied = {}

    for i in range(len(X)):
        for j in range(len(Y)):
            if type(Y[j]) == type(1): # Constant term
                satisfied [i, j] = set(X[i].variables())
            else:
                satisfied [i, j] = set(X[i].variables()).difference(set(Y[j].variables()))
    
    for k in satisfied.values():
        
        if (k) == set(): # "Non-completeness" is not satisfied
            print ('"Non-completeness" NOT satisfied:', satisfied)
            print ('"Non-completeness" NOT satisfied:', satisfied, file=logfile)
            return False
        
    print ('"Non-completeness" satisfied', file=logfile)
    return True


def check_uniformity(Y, X, logfile, uniformity_immediate_abort=True):

    import itertools
    _Y = {}
    X_ = sum(X).variables()
    

    for (_X) in itertools.product([0, 1], repeat=len(X)):
        Y_dict = {(_X): {}}
        
        for (xv) in itertools.product([0, 1], repeat=len(X_)):
            
            # Compute input shares
            __X = tuple([(sum(xv[j*len(Y): (j+1)*len(Y)])%2) for j in range(len(X))])
            
            if (__X) != (_X):
                continue
            
            # Compute output shares
            lcls = locals() # Needed for meta programming
            __Y = []
            ex_str = '__y='
            for idx in range(len(Y)):
                
                if type(Y[idx]) == type(1): # Constant term
                    __Y.append(Y[idx])
                else:
                    ex_str = '__y=(Y['+str(idx)+'](' +\
                    ', '.join([''+str(X_[i])+'=xv['+str(i)+']' for i in range(len(xv))]) + ')' + ')%2'
                    
                    exec(ex_str, None, lcls)
                    __y = lcls["__y"]
                    __Y.append(__y)
            
                
            __Y = tuple(__Y)

            try:
                Y_dict[(__X)][(__Y)] += 1
                
            except KeyError:
                Y_dict[(__X)][(__Y)] = 1

        
        _Y[_X] = Y_dict[_X]

        if uniformity_immediate_abort: # Abort when one row fails
            
            row_uniformity = (set([tuple(y.values()) for y in Y_dict.values()][0]))
            
            if (len(row_uniformity)) != 1:
                print ('Failure', _X, ':', row_uniformity)
                print ('Failure', _X, ':', row_uniformity, Y_dict, file=logfile)
                return False  
    
    unique_frequency = (set(sum([list(y.values()) for y in _Y.values()], [])))
    print ('Success', unique_frequency)
    print ('Success', unique_frequency, file=logfile)
    
    return (len(unique_frequency) == 1)  
    

def wo_decomp_coord(X, Y_, y, shuffle_y=False, shuffle_rhs=False, uniformity_enforced=True, uniformity_immediate_abort=True, shuffle_conflict_X=False):
                              
    shares = len(Y_)
    
    X_conflict = [[] for j in range(shares)] # Conflicting variables for non-completeness
    
    
    for i in range(shares):
        for j in range(len(X)):
            X_conflict[i].append(X[j].variables()[i])

    shares_i = list(range(shares))

    uniformity_check_count = 0

    while True: # Check for uniformity

        if shuffle_conflict_X:
            import random
            random.shuffle(X_conflict)

        print ('\tConflicting (index):', ['_'+(str(x_c[0]).split('_')[1]) for x_c in X_conflict], end='. ')
        print ('\tConflicting:', X_conflict, file=logfile)


        Y = [0]*shares
        Unused_Y_m =  y.monomials()[:]

        if shuffle_rhs: # Shuffle output shares
            import random
            random.shuffle(Unused_Y_m)
        
        while len(Unused_Y_m) > 0: # Assign all output-share monomials
            
            if shuffle_y: # Shuffle input shares
                import random
                random.shuffle(shares_i) 

            for i in shares_i:
                
                if len(Unused_Y_m) == 0:
                    break
                
                monomial = Unused_Y_m[0]        
                
                variables = monomial.variables()
                
                if len(set(variables).intersection(set(X_conflict[i]))) == 0: # Non-complete
                    Y[i] += monomial
                    Unused_Y_m.remove(monomial)
        

        print ('Sharing generated', end='.')
        print ('\tCurrent sharing:', Y, end='.', file=logfile)
        
        
        if uniformity_enforced == False:
            print (end='\n'); print (end='\n', file=logfile)
            break
        else: 
            uniformity_check_count += 1
            print ('\tUniformity check', (uniformity_check_count), end=". ")
            print ('\tUniformity check', (uniformity_check_count), end=". ", file=logfile)

            
            if check_uniformity(Y=Y, X=X, logfile=logfile, uniformity_immediate_abort=uniformity_immediate_abort):
                break
            else:
                shuffle_y = True
                shuffle_rhs = True
                shuffle_conflict_X = True
                
        
    return Y
    
def wo_decomposition(sbx, shares, shuffle_y=True, shuffle_rhs=False, uniformity_enforced=True, uniformity_immediate_abort=True, shuffle_conflict_X=False, logfile='wo_decomp_log.txt'):
    
    size = sbx.n
    
    # Work with one coordinate function at a time
    for index in range(size):

        BX = BooleanPolynomialRing(1+(shares)*(size), ['y%d'%(index)] + ['x%d_%d'%(i, j) for i in range(size) for j in range(shares)])
        XY = BX.gens()
        
        X = [[] for i in range(size)]
        y = XY[0]
        X_ = XY[1 : (size)*shares + 1]
        
        Y_ = BooleanPolynomialRing((shares), ['y%d_%d'%(index, j) for j in range (shares)]).gens()
        
        
        print ('------------------------------------------')
        print ('\tCoordinate index: %d'%index)
        print ('\tOutput variables (before and after sharing):', (y), '=', sum(Y_))
        print ('\tInput variables (after sharing):', X_)

        print ('------------------------------------------', file=logfile)
        print ('\tCoordinate index: %d'%index, file=logfile)
        print ('\tOutput variables (before and after sharing):', (y), '=', sum(Y_), file=logfile)
        print ('\tInput variables (after sharing):', X_, file=logfile)
        
        assert len(X_) == size*shares

        
        print ('\tTarget coordinate function (before sharing):', y, '=', (sbx.component_function(2**index).algebraic_normal_form()))
        print ('\tTarget coordinate function (before sharing):', y, '=', (sbx.component_function(2**index).algebraic_normal_form()), file=logfile)

        
        for i in range(size):
            X[i] = sum(X_[i*shares:(i+1)*shares])
        
        assert sum(X).variables() == X_
        
        import functools
        XX = vector([1] + [functools.reduce(lambda a,b: a*b, x) for x in tuple(powerset(X))[1:]])
        
        z = 0
        c = coordinate_encoding(sbx=sbx, size=size)[index]
        for j in range(len(c)):
            if c[j] != 0:
                z += XX[j]
        y = z

        print ('\tTarget coordinate function (after sharing):', sum(Y_), '=', y)
        print ('\tTarget coordinate function (after sharing):', sum(Y_), '=', y, file=logfile)
        print ('---------------------')
        print ('---------------------', file=logfile)    
        
        Z = wo_decomp_coord(X=X, Y_=Y_, y=y, shuffle_y=shuffle_y, shuffle_rhs=shuffle_rhs, uniformity_enforced=uniformity_enforced, uniformity_immediate_abort=uniformity_immediate_abort,shuffle_conflict_X=shuffle_conflict_X)

        assert check_correctness(Y=Z, y=y, logfile=logfile)
        assert check_incompleteness(Y=Z, X=X, logfile=logfile)
         
        for i in range(shares):
            print ('\x1B[32m' + str(Y_[i]), '=', end=' ')
            print (Y_[i], '=', end=' ', file=logfile)
            if type(Z[i]) == type(1):
                print (Z[i], '\x1B[0m\x1B[31m(zero sharing)', '\x1B[0m')
                print (Z[i], '(zero sharing)', file=logfile)

            else:
                print (Z[i], '\x1B[0m\x1B[33m('+str(len(Z[i].monomials()))+')', '\x1B[0m')
                print (Z[i], '('+str(len(Z[i].monomials()))+')', file=logfile)


def get_go(target_sbx, ti_order, logfile, shuffle_y=True, shuffle_rhs=True, uniformity_enforced=True, uniformity_immediate_abort=True, shuffle_conflict_X=False):

    import datetime, socket
        
    print ('Start:', datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S'), end="\t")
    print ('==========================================================', file=logfile)
    print ('Start:', datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S'), end="\t", file=logfile)
    print ('Host:', socket.gethostname())
    print ('Host:', socket.gethostname(), file=logfile)

    assert ti_order >= 1
    print ('SBox =', target_sbx)
    print ('SBox =', target_sbx, file=logfile)

    shares = target_sbx.max_degree() + ti_order
    print ('Shares =', shares, "(TI order = %d)"%ti_order)
    print ('Shares =', shares, "(TI order = %d)"%ti_order, file=logfile)

    wo_decomposition(sbx=target_sbx, shares=shares, shuffle_y=shuffle_y, shuffle_rhs=shuffle_rhs, uniformity_enforced=uniformity_enforced, uniformity_immediate_abort=uniformity_immediate_abort, shuffle_conflict_X=shuffle_conflict_X, logfile=logfile)


if __name__ =='__main__':

    target_sbx = sage.crypto.sbox.SBox((0,3,2,1,4,7,5,6))
    
    ti_order = 1 # Number of shares = algebraic degree + `ti_order`

    logfile = open('wo_decomp_log.txt', 'a+', buffering=1)
    
    get_go(target_sbx=target_sbx, ti_order=ti_order, logfile=logfile, shuffle_y=True, shuffle_rhs=True, uniformity_enforced=False, uniformity_immediate_abort=True, shuffle_conflict_X=False)
    
    print ("\n", file=logfile)
    logfile.close()
