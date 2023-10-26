# Tested in Sage 9.3
# Generates Table 1(a) of paper

R = BooleanPolynomialRing(3+3*2+2+1, names=['y%d'%d for d in range(3)]+['x%d%d'%(i, j) for i in range(2) for j in range(3)]+['x0', 'x1']+['y'])

R.inject_variables(verbose=False)


x0 = x00 + x01 + x02
x1 = x10 + x11 + x12


y = x0 * x1

y0 = x01 * x11 + x01 * x12 + x02 * x11 # Missing: x00, x10  
y1 = x02 * x12 + x00 * x12 + x02 * x10 # Missing: x01, x11
y2 = x00 * x10 + x00 * x11 + x01 * x10 # Missing: x02, x12

# Confirm missing variables
assert x00 not in y0.variables() and x10 not in y0.variables()
assert x01 not in y1.variables() and x11 not in y1.variables()
assert x02 not in y2.variables() and x12 not in y2.variables()

assert y == y0 + y1 + y2

_Y = {}

import itertools
for (_X0, _X1) in itertools.product([0, 1], repeat=2):
    Y_dict = {(_X0, _X1): {}}
    
    for (x_00, x_01, x_02, x_10, x_11, x_12) in itertools.product([0, 1], repeat=6):
        
        if (x_00 + x_01 + x_02) % 2 != _X0 or (x_10 + x_11 + x_12) % 2 != _X1:
            continue

        _y = y(x00=x_00, x01=x_01, x02=x_02, x10=x_10, x11= x_11, x12=x_12) % 2
        _y0 = y0(x01=x_01, x02=x_02, x11=x_11, x12=x_12) % 2
        _y1 = y1(x00=x_00, x02=x_02, x10=x_10, x12=x_12) % 2
        _y2 = y2(x00=x_00, x01=x_01, x10=x_10, x11=x_11) % 2

        assert (_y0 + _y1 + _y2) % 2 == _y

        try:
            Y_dict[(_X0, _X1)][(_y0, _y1, _y2)] += 1
            
        except KeyError:
            Y_dict[(_X0, _X1)][(_y0, _y1, _y2)] = 1


    _Y[(_X0, _X1)] = Y_dict[(_X0, _X1)]


for k in _Y.keys():
    print (k, ':', _Y[k])

print ("Uniformity is satisfied:", len(set(sum([list(y.values()) for y in _Y.values()], []))) == 1)
