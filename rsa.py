import hashlib
import Crypto.Util.number 
from Crypto.Util.number import inverse

# Generation Des Clé
def gen_rsa_key(bits):
    p = Crypto.Util.number.getPrime(bits//2);
    q = Crypto.Util.number.getPrime(bits//2);
    assert(p != q)
    n = p * q
    e = 65537
    phi_n = (p - 1) * (q - 1);
    d = inverse(e,phi_n)

    return ((e,n),(d,n))

def rsa(message,key):
    return pow(message,key[0],key[1]) 

# Chiffrement
def rsa_enc(m,key):
    enc_m = int.from_bytes(m.encode('utf-8'),'big')
    return rsa(enc_m,key)

# Dechiffrement
def rsa_dec(enc_m,key):
    dec_m = rsa(enc_m,key)
    return dec_m.to_bytes((dec_m.bit_length() + 7) // 8, 'big').decode('utf-8')

# Fonction De Hashage
def hachage(int_m):
    n = int_m.to_bytes((int_m.bit_length() + 7) // 8, 'big')
    m = hashlib.sha256(n).hexdigest()
    return m

# Signature Du Message
def rsa_sign(m,key):
    int_m = int.from_bytes(m.encode('utf-8'),'big')
    h_m = hachage(int_m);
    sign_m = rsa_enc(h_m,key)
    return (m,sign_m)

# Vérification du message
def rsa_verify(sign_m,m,key):
    int_m = int.from_bytes(m.encode('utf-8'),'big')
    v = rsa_dec(sign_m,key)
    h_m = hachage(int_m)
    if(v == h_m):
        print("La signature est correct !\n")
    else:
        print("La signature est incorrect !\n")

