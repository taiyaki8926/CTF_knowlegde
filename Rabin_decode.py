def legendre_symbol(a, p):
    ls = pow(a, (p - 1) // 2, p)
    return -1 if ls == p - 1 else ls

def modular_sqrt(a, p):
    if legendre_symbol(a, p) != 1:
        return 0
    elif a == 0:
        return 0
    elif p == 2:
        return 0
    elif p % 4 == 3:
        return pow(a, (p + 1) / 4, p)
    
    s = p - 1
    e = 0
    while s % 2 == 0:
        s = s // 2
        e += 1
    n = 2
    while legendre_symbol(n, p) != -1:
        n += 1
    x = pow(a, (s + 1) // 2, p)
    b = pow(a, s, p)
    g = pow(n, s, p)
    r = e
    
    while True:
        t = b
        m = 0
        for m in range(r):
            if t == 1:
                break
            t = pow(t, 2, p)
        if m == 0:
            return x
        gs = pow(g, 2 ** (r - m - 1), p)
        g = (gs * gs) % p
        x = (x * gs) % p
        b = (b * g) % p
        r = m


def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)


c = 196353764385075548782571270052469419021844481625366305056739966550926484027148967165867708531585849658610359148759560853
p = 5411451825594838998340467286736301586172550389366579819551237
q = 5190863621109915362542582192103708448607732254433829935869841

def dec(t):
    mp = modular_sqrt(t, p)
    mq = modular_sqrt(t, q)
    _, yp, yq = egcd(p, q)
    r = (yp * p * mq + yq * q * mp) % n
    s = (yp * p * mq - yq * q * mp) % n
    ms = [r, s, n - r, n - s]
    return ms

pow(dec(c)[], 2, p*q) == c
