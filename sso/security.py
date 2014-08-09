import hashlib
import random

class AccessMode(object):
    NORMAL = 'normal'
    MASTER = 'master'

class PasswordService(object):
    ascii_code_a = 65
    ascii_code_0 = 48
    number_count = 10
    alphabet_count = 26
    salt_length  = 32

    def random_salt(self):
        salt_seq = []

        for i in range(self.salt_length):
            use_int   = random.randrange(0, 2)
            salt_byte = random.randrange(0, self.number_count) + self.ascii_code_0 \
                if use_int == 1 \
                else random.randrange(0, self.alphabet_count) + self.ascii_code_a

            salt_seq.append(chr(salt_byte))

        return ''.join(salt_seq)

    def compute(self, plain_password, salt):
        pattern = '{salt}{plain}'.format(
            plain = plain_password,
            salt  = salt
        )

        hasher = hashlib.new('SHA512')
        hasher.update(pattern)

        return hasher.hexdigest()