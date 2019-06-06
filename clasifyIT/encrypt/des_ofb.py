
#Converter from plain text to binary
def plaintobin(msg):
    return ''.join(format(ord(x), 'b').zfill(8) for x in msg)

#S-box "dispenser" function, used in the encryption function
def s_box():
    s1=[[14,4,13,1,2,15,11,8,3,10,6,12,5,9,0,7],
    [0,15,7,4,14,2,13,1,10,6,12,11,9,5,3,8],
    [4,1,14,8,13,6,2,11,15,12,9,7,3,10,5,0],
    [15,12,8,2,4,9,1,7,5,11,3,14,10,0,6,13]]
    s2=[[15,1,8,14,6,11,3,4,9,7,2,13,12,0,5,10],
    [3,13,4,7,15,2,8,14,12,0,1,10,6,9,11,5],
    [0,14,7,11,10,4,13,1,5,8,12,6,9,3,2,15],
    [13,8,10,1,3,15,4,2,11,6,7,12,0,5,14,9]]
    s3=[[10,0,9,14,6,3,15,5,1,13,12,7,11,4,2,8],
    [13,7,0,9,3,4,6,10,2,8,5,14,12,11,15,1],
    [13,6,4,9,8,15,3,0,11,1,2,12,5,10,14,7],
    [1,10,13,0,6,9,8,7,4,15,14,3,11,5,2,12]]
    s4=[[7,13,14,3,0,6,9,10,1,2,8,5,11,12,4,15],
    [13,8,11,5,6,15,0,3,4,7,2,12,1,10,14,9],
    [10,6,9,0,12,11,7,13,15,1,3,14,5,2,8,4],
    [3,15,0,6,10,1,13,8,9,4,5,11,12,7,2,14]]
    s5=[[2,12,4,1,7,10,11,6,8,5,3,15,13,0,14,9],
    [14,11,2,12,4,7,13,1,5,0,15,10,3,9,8,6],
    [4,2,1,11,10,13,7,8,15,9,12,5,6,3,0,14],
    [11,8,12,7,1,14,2,13,6,15,0,9,10,4,5,3]]
    s6=[[12,1,10,15,9,2,6,8,0,13,3,4,14,7,5,11],
    [10,15,4,2,7,12,9,5,6,1,13,14,0,11,3,8],
    [9,14,15,5,2,8,12,3,7,0,4,10,1,13,11,6],
    [4,3,2,12,9,5,15,10,11,14,1,7,6,0,8,13]]
    s7=[[4,11,2,14,15,0,8,13,3,12,9,7,5,10,6,1],
    [13,0,11,7,4,9,1,10,14,3,5,12,2,15,8,6],
    [1,4,11,13,12,3,7,14,10,15,6,8,0,5,9,2],
    [6,11,13,8,1,4,10,7,9,5,0,15,14,2,3,12]]
    s8=[[13,2,8,4,6,15,11,1,10,9,3,14,5,0,12,7],
    [1,15,13,8,10,3,7,4,12,5,6,11,0,14,9,2],
    [7,11,4,1,9,12,14,2,0,6,10,13,15,3,5,8],
    [2,1,14,7,4,10,8,13,15,12,9,0,3,5,6,11]]
    return {'1':s1,'2':s2,'3':s3,'4':s4,'5':s5,'6':s6,'7':s7,'8':s8}

#A function that contains permutation tables for the DES cipher
def permutaion_table():
    ip=[[58,50,42,34,26,18,10,2],
    [60,52,44,36,28,20,12,4],
    [62,54,46,38,30,22,14,6],
    [64,56,48,40,32,24,16,8],
    [57,49,41,33,25,17,9,1],
    [59,51,43,35,27,19,11,3],
    [61,53,45,37,29,21,13,5],
    [63,55,47,39,31,23,15,7]]
    fp=[[40,8,48,16,56,24,64,32],
    [39,7,47,15,55,23,63,31],
    [38,6,46,14,54,22,62,30],
    [37,5,45,13,53,21,61,29],
    [36,4,44,12,52,20,60,28],
    [35,3,43,11,51,19,59,27],
    [34,2,42,10,50,18,58,26],
    [33,1,41,9,49,17,57,25]]
    exp=[[32,1,2,3,4,5],
    [4,5,6,7,8,9],
    [8,9,10,11,12,13],
    [12,13,14,15,16,17],
    [16,17,18,19,20,21],
    [20,21,22,23,24,25],
    [24,25,26,27,28,29],
    [28,29,30,31,32,1]]
    p=[[16,7,20,21,29,12,28,17],
    [1,15,23,26,5,18,31,10],
    [2,8,24,14,32,27,3,9],
    [19,13,30,6,22,11,4,25]]
    key_parity=[[57,49,41,33,25,17,9,1],
    [58,50,42,34,26,18,10,2],
    [59,51,43,35,27,19,11,3],
    [60,52,44,36,63,55,47,39],
    [31,23,15,7,62,54,46,38],
    [30,22,14,6,61,53,45,37],
    [29,21,13,5,28,20,12,4]]
    key_permute=[[14,17,11,24,1,5,3,28],
    [15,6,21,10,23,19,12,4],
    [26,8,16,7,27,20,13,2],
    [41,52,31,37,47,55,30,40],
    [51,45,33,48,44,49,39,56],
    [34,53,46,42,50,36,29,32]]
    return {'initial':ip,'final':fp,'exp':exp,'p':p,'pc1':key_parity,'pc2':key_permute}
    
def permutation(text,table,row,col):
    st=""
    for i in range(row):
        for j in range(col):
            st+=text[table[i][j]-1]
    return st

def xor(l,r,length):
    st=str(bin(int(l,2)^int(r,2)))[2:]
    if len(st)<length:
        while len(st) <length:
            st='0'+st
    return st

#The main function that is used for the encryption and decryption procedure.
def function(r,key):
    #Create local vars and table "dispensers"
    st=""
    table=permutaion_table()
    exp=permutation(r,table['exp'],8,6)
    xored=xor(exp,key,48)
    s_boxes=s_box()
    st=s_box_compression(xored,s_boxes)
    
    return permutation(st,table['p'],4,8)

def s_box_compression(msg,s_box):
    st=""
    s_num=1
    for i in range(0,len(msg),6):
        chunk=msg[i:i+6]
        row=int(chunk[0]+chunk[5],2)
        col=int(chunk[1:5],2)
        
        table=bin(int(s_box[str(s_num)][row][col]))[2:]
        res=str(table).zfill(4)
        st+=res
        s_num+=1
    return st

def generate_keys(key):
    keys=[]
    final_keys=[]
    table=permutaion_table()
    ckey=permutation(key,table['pc1'],7,8)
    key_left,key_right=ckey[0:28],ckey[28:56]
    keys.append(leftshift(key_left,1)+leftshift(key_right,1))
    ckey=keys[0]
    for i in range(2,17):
        if i in [1,2,9,16]:
            key_left,key_right=ckey[0:28],ckey[28:56]
            keys.append(leftshift(key_left,1)+leftshift(key_right,1))
            ckey=keys[i-1]
        else:
            key_left,key_right=ckey[0:28],ckey[28:56]
            keys.append(leftshift(key_left,2)+leftshift(key_right,2))
            ckey=keys[i-1]
    for i in range(16):
        final_keys.append(permutation(keys[i],table['pc2'],6,8))
    return final_keys

def reverse_keys(key):
    reversed_keys=[]
    j=15
    for i in range(16):
        reversed_keys.append(key[j-i])
    return reversed_keys

def des_encrypt(plain,key):
    cypher=""
    code=plaintobin(plain)
    key=plaintobin(key)
    pkey=generate_keys(key)
    table=permutaion_table()
    pcode=permutation(code,table['initial'],8,8)
    for i in range(16):
        left, right = pcode[0:32], pcode[32:64]
        temp=left
        left=right
        right=xor(temp,function(right,pkey[i]),32)
        pcode=right+left
    cypher=permutation(pcode,table['final'],8,8)
    return binary_string(cypher)

#Simple left-rotating function
def leftshift(key,count):
    for i in range(count):
        key+=key[0]
        key=key[1:]
    return key

def des_decrypt(code,key):
    plaintext=""
    cipher=plaintobin(code)
    key=plaintobin(key)
    table=permutaion_table()
    pcode=permutation(cipher,table['initial'],8,8)
    pkey=reverse_keys(generate_keys(key))
    for i in range(16):
        left, right = pcode[0:32], pcode[32:64]
        temp=left
        left=right
        right=xor(function(right,pkey[i]),temp,32)
        pcode=right+left
    plaintext=permutation(pcode, table['final'], 8, 8)
  
    return binary_string(plaintext)


def binary_string(s):
    return ''.join(chr(int(s[i*8:i*8+8],2)) for i in range(len(s)//8))


def split_to_blocks(plaintext):
    text = [plaintext[i:i+8] for i in range(0, len(plaintext), 8)]
    if len(text[-1])<8:
        while len(text[-1])<8:
            text[-1]+=" "
    return text


def ofb_encrypt(code,key,iv):
    blocks=split_to_blocks(code)
    result=""
    for block in blocks:
        iv=des_encrypt(iv,key)
        bin_iv=plaintobin(iv)
        bin_block=plaintobin(block)
        xored=binary_string(xor(bin_block,bin_iv,64))
        result+=xored
    return result

def ofb_decrypt(cipher,key,iv):
    blocks=split_to_blocks(cipher)
    result=""
    for block in blocks:
        iv=des_encrypt(iv,key)
        bin_iv=plaintobin(iv)
        bin_block=plaintobin(block)
        xored=binary_string(xor(bin_block,bin_iv,64))
        result+=xored
    return result
