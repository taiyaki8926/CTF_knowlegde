# given n, g, c
n = ...
g = ...
c = ...

# to factorize n, use "factordb.com"
p = ...
q = ...

def L(u):
    return (u-1) // n

# extended Euclidean algorithm
def egcd(e, n):
    x, y, u, v = 0, 1, 1, 0
    while e != 0:
        q, r = n // e, n % e
        m, n = x - u * q, y - v * q
        n, e, x, y, u, v = e, r, u, v, m, n
    return x
    
def decrypt_Paillier(n, g, c, p, q):
    import math
    import codecs
    _lambda = (p-1) * (q-1) // math.gcd(p-1, q-1)
    m = L(pow(c, _lambda, n**2)) * egcd(L(pow(g, _lambda, n**2)), n) % n
    return codecs.decode(('%x' % m), 'hex_codec')
