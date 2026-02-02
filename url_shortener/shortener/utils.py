import string

BASE62 = string.digits + string.ascii_letters

def encode_base62(num):
    if num == 0:
        return BASE62[0]

    base = len(BASE62)
    encoded = []

    while num:
        num, rem = divmod(num, base)
        encoded.append(BASE62[rem])

    return ''.join(reversed(encoded))
