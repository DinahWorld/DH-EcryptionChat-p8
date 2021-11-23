import random
import Crypto.Util.number 

# On séléctionne un nombre premier  et on génere un nombre g inférieur a p - 1 et 
# supérieur à 0
def gen_dh(bits):
    p = Crypto.Util.number.getPrime(bits//2);
    g = random.randint(0,p - 1)
    return (p,g)

# On genere un nombre aléatoire secret inférieur a p - 1 et supérieur à 0 
def secret_value_gen(p):
    return random.randint(0,p-1)

# On calcule notre clé publique avec les valeurs généré auparavant
def dh_public_key(g,secret_value,p):
    return pow(g,secret_value,p)

# Une fois la clé généré on la partage à notre interlocuteur    
def dh_private_key(public_key,secret_value,p):
    return pow(public_key,secret_value,p)

# On chiffre notre message
def dh_enc(msg,private_key,p):
    enc_m = int.from_bytes(msg.encode('utf-8'),'big')
    return pow(enc_m + private_key,1,p)

# On déchiffre notre message
def dh_dec(msg,private_key,p):
    dec_m = pow(msg - private_key,1,p)
    return dec_m.to_bytes((dec_m.bit_length() + 7) // 8, 'big').decode('utf-8')

