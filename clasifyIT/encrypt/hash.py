mask = 0xffffffff
import bcrypt

def manage(message):
    salt_to_db = bcrypt.gensalt().decode()
    return hash(message + salt_to_db ) , salt_to_db


def hash(string):
    def preprocess():
        """""
        function to preprocess the string by appanding to it 1 and zeros and making a bit string
        """""
        # to bitstring string+ append 1 bit to the end
        data = "".join([bin(ord(char))[2:].zfill(8) for char in string] + ["1"])
        # append zeros
        bitlen = len(data)
        data += "0" * ((448 - bitlen % 512) if bitlen % 512 < 448 else (512 + (448 - len(data) % 512)))
        data += bin(len(string) * 8)[2:].zfill(64)
        return data

    def update_hashs():
        """
        function to update the hash values
        :return:
        """
        nonlocal hash_values
        hash_values['h0'] += registers['a']
        hash_values['h1'] += registers['b']
        hash_values['h2'] += registers['c']
        hash_values['h3'] += registers['d']
        hash_values['h4'] += registers['e']
        hash_values['h5'] += registers['f']
        hash_values['h6'] += registers['g']
        hash_values['h7'] += registers['h']

    functools = {'rs': lambda x, y: x >> y,
                 'rr': lambda x, y: ((x >> y) | (x << (32 - y))) & mask,
                 'chunks': lambda massage, chunk_size: [massage[i:i + chunk_size] for i in
                                                        range(0, len(massage), chunk_size)]
                 }

    def compress():
        """
         Compression function main loop
        :return:
        """
        for i in range(0, 64):
            s1 = functools['rr'](registers['e'], 6) ^ functools['rr'](registers['e'], 11) ^ \
                 functools['rr'](registers['e'], 25)
            ch = registers['g'] ^ (registers['e'] & (registers['f'] ^ registers['g']))
            temp1 = registers['h'] + s1 + ch + k[i] + w[i]
            s0 = functools['rr'](registers['a'], 2) ^ functools['rr'](registers['a'], 13) \
                 ^ functools['rr'](registers['a'], 22)
            maj = (registers['a'] & registers['b']) ^ (registers['a'] & registers['c']) \
                  ^ (registers['b'] & registers['c'])
            temp2 = s0 + maj

            registers['h'] = registers['g']
            registers['g'] = registers['f']
            registers['f'] = registers['e']
            registers['e'] = registers['d'] + temp1 & mask
            registers['d'] = registers['c']
            registers['c'] = registers['b']
            registers['b'] = registers['a']
            registers['a'] = temp1 + temp2 & mask

    def sha_process():
        """
        :return:
        """
        nonlocal w

        s = lambda x, y, z, v: functools['rr'](w[i - x], y) ^ functools['rr'](w[i - x], z) ^ functools['rs'](
            w[i - x], v)

        # Process the message in successive 512-bit chunks:
        for chunk in functools['chunks'](preprocess(), 512):
            # create a 64-entry message schedule array w[0..63] of 32-bit words
            w = [0] * 64
            words = functools['chunks'](chunk, 32)
            # copy chunk into first 16 words w[0..15] of the message schedule array
            w[:16] = [int(n, 2) for n in words]
            print(w[:16])
            # Extend the first 16 words into the remaining 48 words w[16..63] of the message schedule array:
            for i in range(16, 64):
                w[i] = (w[i - 16] + s(15, 7, 18, 3) + w[i - 7] + s(2, 17, 19, 10)) & mask

            compress()

            update_hashs()

    k = [
        0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
        0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
        0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
        0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
        0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
        0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
        0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
        0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2]
    hash_values = {'h0': 0x6a09e667,
                   'h1': 0xbb67ae85,
                   'h2': 0x3c6ef372,
                   'h3': 0xa54ff53a,
                   'h4': 0x510e527f,
                   'h5': 0x9b05688c,
                   'h6': 0x1f83d9ab,
                   'h7': 0x5be0cd19}
    w = None
    # Initialize working variables to current hash value
    registers = {'a': hash_values['h0'],
                 'b': hash_values['h1'],
                 'c': hash_values['h2'],
                 'd': hash_values['h3'],
                 'e': hash_values['h4'],
                 'f': hash_values['h5'],
                 'g': hash_values['h6'],
                 'h': hash_values['h7']}
    sha_process()
    return '%08x%08x%08x%08x%08x%08x%08x%08x' % (
        hash_values['h0'] & mask, hash_values['h1'] & mask,
        hash_values['h2'] & mask, hash_values['h3'] & mask,
        hash_values['h4'] & mask, hash_values['h5'] & mask,
        hash_values['h6'] & mask, hash_values['h7'] & mask)


