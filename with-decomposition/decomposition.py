
# Tested in Sage 9.3

from sage.crypto.sbox import SBox

# Quadratic classes from Begül Bilgin's thesis: 4, 12, 293, 294, 299, 300
CLASS_004 = SBox(map(lambda z: int(z, 16), '0123456789ABDCFE'))
CLASS_012 = SBox(map(lambda z: int(z, 16), '0123456789CDEFAB'))
CLASS_293 = SBox(map(lambda z: int(z, 16), '0123457689CDEFBA'))
CLASS_294 = SBox(map(lambda z: int(z, 16), '0123456789BAEFDC'))
CLASS_299 = SBox(map(lambda z: int(z, 16), '012345678ACEB9FD'))
CLASS_300 = SBox(map(lambda z: int(z, 16), '0123458967CDEFAB'))


def get_int_to_bin_vector(x, l=4):
    return vector(GF(2), map(lambda z: z == '1', (bin(x)[2:]).zfill(l)))

def get_bin_vector_to_int(x):
    return int('0b' + ''.join(map(lambda z: str(z), x)), 2)

def get_affine_sbox(S):
    random_mat = zero_matrix(GF(2), S.n)
    while not random_mat.is_invertible():
        random_mat = random_matrix(GF(2), S.n)
    
    random_vec = random_vector(GF(2), S.n)
    
    random_mat2 = zero_matrix(GF(2), S.n)
    while not random_mat2.is_invertible():
        random_mat2 = random_matrix(GF(2), S.n)
    
    random_vec2 = random_vector(GF(2), S.n)


    from math import pow
    T = [None]*(int(pow(2, S.n)))
    for x in range(int(pow(2, S.n))):
        
        Y = S[get_bin_vector_to_int((random_mat * get_int_to_bin_vector(x, l=S.n)) + random_vec)]
        X = get_bin_vector_to_int((random_mat2 * get_int_to_bin_vector(Y, l=S.n)) + random_vec2)

        T[x] = X
            
    return SBox(T)


def tohex(x, join_char=','):
    return join_char.join(list(map(lambda z: (hex(z)[2:]).upper(), list(x))))


def generate_decompostions(S, order=2, base_in=None, ineq_type="<"):
    
    while(True):
        
        if type(base_in) == type(None):
            if S.n == 4:
                import random
                base = random.choice((CLASS_004, CLASS_012, CLASS_293, CLASS_294, CLASS_299, CLASS_300)) ## Degree classes
            else:
                raise NotImplementedError            
        else:
            base = base_in
        
        Gs = [None]*(order-1)

        for g in range(order-1):
            Gs[g] = get_affine_sbox(S=base)
        
        
        F = [None]*len(list(Gs[0]))
        
        y = []
        for i in range(int(pow(2, S.n))):
            x = i
            for j in range(len(Gs))[::-1]:
                
                x = Gs[j][x]

            y.append(x) # Composition of all but 1 SBox

        for i in S:
            r = y[i]    
            F[r] = S[i]
        
        F = SBox(F)

        if ineq_type == "<":
            if F.max_degree() < S.max_degree() and max(map(lambda z: z.max_degree(), Gs)) < S.max_degree():
                break
        elif ineq_type == "<=":
            if F.max_degree() <= S.max_degree() and max(map(lambda z: z.max_degree(), Gs)) <= S.max_degree():
                break
        else:
            raise AssertionError
    FG = [F]
    FG.extend(Gs)
    return FG, base

def get_min_cost_decompositions(S, ineq_type="<", count=1, order=2, base_in=None, log='decomp_log.txt'):

    out = open(log, 'a+')
    
    out.write("\n" + tohex(S) + ": ")
    out.flush()
    c = 0

    while (c < count):
        c += 1  
        FG, base = generate_decompostions(S=S, ineq_type=ineq_type, base_in=base_in, order=order) 

        for fg in FG:
            out.write(tohex(fg))
            out.write('; ')
        out.flush()

    out.close()

    return FG, base

if __name__ == '__main__':

    # Import pre-defined SBoxes
    from sage.crypto.sboxes import PRESENT as PRESENT_SBOX
    from sage.crypto.sboxes import SKINNY_4 as SKINNY_SBOX
    from sage.crypto.sboxes import GIFT as GIFT_SBOX


    target_sbx = SKINNY_SBOX

    print (tohex(target_sbx, join_char=''), '('+str(target_sbx.max_degree())+')')
    
    FGs, base = get_min_cost_decompositions (S=target_sbx, count=1, order=2, ineq_type="<", base_in=None, log="decomp_log.txt")

    print (tuple(map( lambda z: (tohex(z, join_char=''), (z.max_degree())), FGs)))
    
    