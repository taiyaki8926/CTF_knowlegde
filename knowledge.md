# Crypto

## Paillier Crypto System
Link : https://en.wikipedia.org/wiki/Paillier_cryptosystem

(Unlike RSA encryption,) when `n`, `g` and `c` are given, it should be inferred that the Paillier encryption method is used.

```Python3:Paillier.py

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
    return codecs.decode(('%x'%m), 'hex_codec')
```

## Pohlig-Hellman Algorithm

Link : https://en.wikipedia.org/wiki/Pohlig–Hellman_algorithm

Given `g`, `h`, and `G`, and find `x` that satisfies

`g ^ x = h (mod G)`

This is called the "discrete logarithm problem", and it is difficult to find `x`. However, if the order of `g`, that is, the minimum value of `n` satisfying

`g ^ n = 1 (mod G)`

can be represented by the product of simple prime factors - like `n = p ^ e`, then Pohlig-Hellman's algorithm can be used to find `x` easily.

```Python3:Pohlig-Hellman.py

# Given g, h, G
g = ...
h = ...
G = ...

# find n, the order of g
import sympy as sym
n = sym.n_order(g, G)

# factorize n
p = ...
e = ...

def Pohlig-Hellman(g, p, e, h, G):
    from Crypto.Util.number import inverse
    x = [0]
    gamma = pow(g, p ** (e-1), G)
    for k in range(e):
        h_k = (pow(inverse(g, G), x[k], G) * h) % G
        h_k = pow(h_k, p ** (e-1-k), G)
        if h_k == gamma:
            d_k = 1
        else:
            d_k = 0
        x.append(x[k] + (p ** k) * d_k)
    retrun x[-1]
```
