from Crypto.Util.number import isPrime

def legendre_symbol(n, p):
    ls = pow(n, (p - 1) // 2, p)
    if ls == 1:
        return 1
    elif ls == p - 1:
        return -1
    else:
        # in case ls == 0
        raise Exception('n:{} = 0 mod p:{}'.format(n, p))

def check_sqrt(x, n, p):
    assert(pow(x, 2, p) == n % p)

def modular_sqrt(n:int, p:int) -> list:
    if type(n) != int or type(p) != int:
        raise TypeError('n and p must be integers')

    if p < 3:
        raise Exception('p must be equal to or more than 3')

    if not isPrime(p):
        raise Exception('p must be a prime number. {} is a composite number'.format(p))

    if legendre_symbol(n, p) == -1:
        raise Exception('n={} is Quadratic Nonresidue modulo p={}'.format(n, p))

    if p % 4 == 3:
        x = pow(n, (p + 1) // 4, p)
        check_sqrt(x, n, p)
        return [x, p - x]

    # Tonelli-Shanks
    q, s = p - 1, 0
    while q % 2 == 0:
        q //= 2
        s += 1
    z = 2
    while legendre_symbol(z, p) != -1:
        z += 1
    m, c, t, r = s, pow(z, q, p), pow(n, q, p), pow(n, (q + 1) // 2, p)
    while t != 1:
        pow_t = pow(t, 2, p)
        for j in range(1, m):
            if pow_t == 1:
                m_update = j
                break
            pow_t = pow(pow_t, 2, p)
        b = pow(c, int(pow(2, m - m_update - 1)), p)
        m, c, t, r = m_update, pow(b, 2, p), t * pow(b, 2, p) % p, r * b % p
    check_sqrt(r, n, p)
    return [r, p - r]

print(modular_sqrt(5, 41))
