import random
import uuid
import hashlib


def access_secret(header=''):
    base_string = str(uuid.uuid4())
    base_string += str(random.randint(10000, 99999))
    m = hashlib.md5()
    m.update(base_string.encode('utf-8'))
    secret = m.hexdigest()
    if header:
        secret = header + '_' + secret
    return secret
