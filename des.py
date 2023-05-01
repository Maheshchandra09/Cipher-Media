from Crypto.Cipher import DES 
from secrets import token_bytes

key=token_bytes(8)

def encrypt(msg):
    cipher=DES.new(key,DES.MODE_EAX)
    nonce=cipher.nonce
    ciphertext,tag=cipher.encrypt_and_digest(msg.encode('ascii'))
    return nonce,ciphertext,tag 

def decrypt(nonce,ciphertext,tag):
    cipher=DES.new(key,DES.MODE_EAX,nonce=nonce)
    plaintext=cipher.decrypt(ciphertext)

    try:
        cipher.verify(tag)
        return plaintext.decode('ascii')
    except:
        return false
    
nonce,ciphertext,tag=encrypt(input("enter msg"))
plaintext=decrypt(nonce,ciphertext,tag)

print("cipher text : {}".format(ciphertext))

if not plaintext:
    print("corrupted")
else:
    print("plain text: {}".format(plaintext))