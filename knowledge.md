# Crypto

## mod inverse

```Python3:mod_inv.py
from Crypto.Util.number import inverse

d = inverse(e, phi)
```

## Paillier Crypto System
Link : https://en.wikipedia.org/wiki/Paillier_cryptosystem

(Unlike RSA encryption,) when `n`, `g` and `c` are given, it should be inferred that the Paillier encryption method is used.

See [Paillier_decrypt.py](https://github.com/taiyaki8926/CTF_knowlegde/blob/master/Paillier_decrypt.py)


## Pohlig-Hellman Algorithm

Link : https://en.wikipedia.org/wiki/Pohlig–Hellman_algorithm

Given `g`, `h`, and `G`, and find `x` that satisfies

`g ^ x ≡ h (mod G)`

This is called the "discrete logarithm problem", and it is difficult to find `x`. However, if the order of `g`, that is, the minimum value of `n` satisfying

`g ^ n ≡ 1 (mod G)`

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


## ppencode

Link : https://masutaro.hatenadiary.org/entry/20080128/1201507016 (Only Japanese)

```
perl -e 'hoge'
```

Note that semicolons `'` is required.


## RSA(private key is given)

(Here, I don't mention basic knowledge about RSA.)

The method to derive primes `p` and `q` when the secret key `d` is given, is described below (Naturally `n` and `e` are given).

Firstly, the two following formulas hold (`k` is integer).

・`n = pq`

・`ed ≡ 1 mod (p-1)(q-1)` , i.e. `ed - 1 = k(p-1)(q-1)`

As a lemma, the following holds; Proof is omitted because it is simple.

> Lemma : When `p` > 3 and `q` > 3, 
>
> `1/2 * pq < (p-1)(q-1) < pq`

Using this lemma, 

`n/2 < (ed - 1) / k < n`, i.e. `(ed - 1) / n < k < 2(ed - 1) / n`

Now that the range of `k` has been narrowed, we use brute-force to find the value of `k` such that `(ed - 1) % k == 0`.

When `k` is known, `p + q` can be obtained, and `p`, `q` can also be obtained from Vieta's formula.

```Python3:find_p_q.py
from sympy import *

# Given n, e, d
n = ...
e = ...
d = ...

def find_p_q(n, e, d):
    # check that p is larger than 3 or not
    if n % 2 == 0:
        print("p = 2, q = {}".format(n // 2))
    elif n % 3 == 0:
        print("p = 3, q = {}".format(n // 3))
    else:
        k_min = (e * d - 1) // n
        for k in range(k_min, 2 * k_min + 1):
            if (e * d - 1) % k == 0:
                # phi = (p-1)(q-1)
                phi = (e * d - 1) // k
                # _sum = p + q
                _sum = n - phi  + 1
                x = Symbol('x')
                p, q = solve(x ** 2 - _sum * x + n)
                if p.is_integer:
                    print('p is {}\n'.format(p))
                    print('q is {}'.format(q))
    return 0
```

Among the displayed results, the integer pairs are (`p`, `q`).

## Elliptic Curve

Use [Sage Math Cell](https://sagecell.sagemath.org).

Knowlegde:

・`EllipticCurve(Zmod(n), [a, b])` (or `EllipticCurve(IntegerModRing(n), [a, b])`) means `y ^ 2 = x ^ 3 + ax + b (mod n)`.

・In the elliptic curve EC, multiplication `P' = k * P` with respect to the coordinates of a certain point `P` is defined as follows : 

> Repeat the operation `k − 1` times, “move the point of intersection of tangent and EC at point `P` symmetrically with respect to the `x` axis”.

・Conversely, how to find `P` from `P'` is

`P = k_inv * P`

, where

`k_inv = inverse_mod(k, EC.order())`

is.

・What is `EC.order()`? -> The number of rational points (including infinity) on an elliptic curve.

・However, in Sage Math, `EC.order()` can not be obtained if `n` of `EC = EllipticCurve(Zmod(n), [a, b])` is a composite number.

Therefore, by factoring into `n = p * q` and setting

`EC_p = EllipticCurve(Zmod(p), [a, b])`

`EC_q = EllipticCurve(Zmod(q), [a, b])`

, and `EC.order() = EC_p.order() * EC_q.order()` holds.

## Rabin Crypto System

Under the situation of `n = p * q`, 

Encrypt : `y = pow(x, 2, n)`

This is not a general form, but here we deal with the case of this expression.

Decoding code is posted in [rabin_decrypt.py](https://github.com/taiyaki8926/CTF_knowlegde/blob/master/Rabin_decrypt.py)

Caution!! : There is no single plaintext. There are four possibilities.

## Legendre symbol and Euler's criterion

Euler's criterion : 

 * `pow(a, (p-1)//2, p) == 1 ` <=> There is an integer `x` such that `a ≡ x ^ 2 (mod p)`

 * `pow(a, (p-1)//2, p) == -1 ( or p-1) ` <=> There is no such integer

 * `pow(a, (p-1)//2, p) == 0 ` <=> `a ≡ 0 (mod p)`

### Part 1
If `p ≡ 3 (mod 4)` and `pow(a, (p-1)//2, p) == 1 `, 

`x = ± pow(a, (p+1)//4, p)`

### Part2
Else if `p ≡ 1 (mod 4)` , `pow(a, (p-1)//2, p) == 1 `, and `p` is prime, use [Tonelli–Shanks algorithm](https://en.wikipedia.org/wiki/Tonelli%E2%80%93Shanks_algorithm)

```Python3:Sage.py
# using Sage

from sage.rings.finite_rings.integer_mod import * 

p = Integers(7)
a = IntegerMod(p, 4)

x = square_root_mod_prime(a)
# -> return 2
```

Perhaps it is possible to use this algorithm even if `p` is not a prime number.


### Others
If `p ≡ 3 (mod 4)` and `sympy.n_order(a, p) = (p-1) // 2`, then `a` is quadratic residue, and `-a` is quadratic non-residue

## Trivia

When `N=pq`, `p^k mod N` is a multiple of `p`.

So it is possible to narrow down `p` with the GCD(`p^k mod N`, `N`)

## OpenSSL

### private or public key is given

```Terminal:
$ openssl rsa -in hoge.pem -text -noout

or

$ openssl rsa -in hoge.der -inform der -text -noout

->

modulus: ~
publicExponent: ~
privateExponent: ~
prime1: ~
prime2: ~
exponent1: ~
exponent2: ~
coefficient: ~
```

* modulus : `n`

* publicExponent : `e`

* privateExponent : `d`

* prime1, prime2 : `p, q`

* exponent1, exponent2, coefficient : (not use -> see also the below link)

Link(Only Japanese) : 

https://qiita.com/kunichiko/items/12cbccaadcbf41c72735

https://qiita.com/ch7821/items/4b315902c0c5f84083ab

If you wanna remove the colon, (in other words, if you wanna get a hexdecimal value)

```Terminal:
$ openssl asn1parse -in hoge.pem 

or
 
$ openssl asn1parse -in hoge.der -inform der
```

### Certificate Signing Request(CSR) is given

(Only know the public key, of course.)

```Terminal:
$ openssl x509 -in hoge.pem -text -noout

or 

$ openssl x509 -in hoge.der -inform der -text -noout
```

I don't know how to get rid of colon, so let me know please :(

## Others

### JSF*ck(Esoteric Programming Language)
When the code is written using only six characters: `[`, `]`, `(`, `)`, `!`, and `+`, then it can be decoded on [this site](https://enkhee-osiris.github.io/Decoder-JSFuck/).

### Mnemonic major system
See [here](https://en.wikipedia.org/wiki/Mnemonic_major_system)

### Never gonna give you up
Lyrics : We're no strangers to love, You know the rules 〜


# Forensics

## fcrackzip
If `.png` file and `.zip` file with password are given, 

```
$ strings hoge.png > word_ls.txt
$ fcrackzip -v -D -u -p word_ls.txt fuga.zip
```

## binwalk
No comments, lol :)


# Miscellaneous

## str(not bytes) -> decimal

If you want to convert bytes -> decimal, remove `.encode()` section of the code below.

```Python3:str2decimal.py
_str = 'abc'
int(_str.encode().hex(), 16)

# -> 6382179
```

## decimal -> bytes

```Python3:decimal2bytes.py
import codecs

m = 6382179
codecs.decode(('%x' % m), 'hex_codec')

# -> b'abc'
```


# File Decompression

## POSIX tar archive (GNU)

```
$ tar -xvf hoge.tar
```

-x : eXtract

-v : Verbose (view archive results)

-f : File

## Zip archive data, at least v2.0 to extract

```
$ unzip hoge.zip
```

## bzip2 compressed data, block size = …

```
bunzip2 -k hoge.bz2
```

-k : Keep

## gzip compressed data, …

```
gzip -kd hoge.gz
```

-k : Keep

-d : Decompress

## XZ compressed data

```
$ xz -kd hoge.xz 
```

## RAR archive data, v5

```
$ rar e hoge.rar
```

If RAR file has a password lock, download `rockyou.txt` and execute

```
$ rar2john hoge.rar > rar.hash
$ john --wordlist (Appropriate Directory)/rockyou.txt --format=rar5 rar.hash
$ john --show rar.hash
```
