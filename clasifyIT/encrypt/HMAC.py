
from hashlib import sha256
import random
import string
from .hash import hasher

sha = hasher()['hash']
#function to convert binary numbers to plain text
def binary_string(s):
    return ''.join(chr(int(s[i*8:i*8+8],2)) for i in range(len(s)//8))

#function to convert string to binary
def to_bin(msg):
    return ''.join(format(ord(x), 'b').zfill(8) for x in msg)

#main HMAC function
def hmac(msg,key):
    #variables for padding with the key given to the function
    ipad=format(0x35,'064b')
    opad=format(0x5c,'064b')
    #convert key to binary
    bin_key=to_bin(key)
    #the hashing steps with the ipad variable
    ipad_step=ipad_hmac(msg,ipad,bin_key)
    #padding with the opad variable
    opad_step=opad_hmac(opad,bin_key)

    #final step to make the authentication code
    authentication=sha256((ipad_step+opad_step).encode('utf-8')).hexdigest()

    return authentication

def opad_hmac(opad,key):
    #constant IV variable to hash with the key and opad
    iv="fmYDQrym"
    #xor between the key and the padding
    xored=int(opad,2)^int(key,2)
    #convert the xor back to plain text
    plain=binary_string(format(xored,'064b'))
    #hash the plain xor with the IV
    hashed=sha256((plain+iv).encode('utf-8')).hexdigest()
    return hashed

def ipad_hmac(blocks,ipad,key):
    #Constant IV variable to hash with the key and ipad
    iv="fmYDQrym"
    #xor between the padding and the key
    xored=int(ipad,2)^int(key,2)
    #convert the xor to plain text
    plain=binary_string(format(xored,'064b'))
    #hashing of the plain text with the iv
    hashed=sha256((plain+iv).encode('utf-8')).hexdigest()
    #hashing the hashed result again with the message given
    for msg in blocks:
        hashed=sha256((str(hashed)+msg).encode('utf-8')).hexdigest()
    return hashed


print(hmac("sometext","key"))

def check_authentication(msg,key,code):
    #checks if the authentication code matches the hmac result given with the user details
    if hmac(msg,key)==code:
        return True
    return False

