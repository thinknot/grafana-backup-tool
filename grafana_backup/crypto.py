import base64, hashlib, sys
from Crypto import Random
from Crypto.Cipher import AES


def encrypt(key, raw):
    hashed_key = hashlib.sha256(key.encode()).digest()
    BS = AES.block_size
    pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
    raw = base64.b64encode(pad(raw).encode('utf8'))
    iv = Random.get_random_bytes(AES.block_size)
    cipher = AES.new(key=hashed_key, mode=AES.MODE_CFB, iv=iv)
    a = base64.b64encode(iv + cipher.encrypt(raw))
    IV = Random.new().read(BS)
    aes = AES.new(hashed_key, AES.MODE_CFB, IV)
    b = base64.b64encode(IV + aes.encrypt(a))
    return b


def decrypt(key, enc):
    hashed_key = hashlib.sha256(key.encode()).digest()
    BS = AES.block_size
    passphrase = hashed_key
    encrypted = base64.b64decode(enc)
    IV = encrypted[:BS]
    aes = AES.new(passphrase, AES.MODE_CFB, IV)
    enc = aes.decrypt(encrypted[BS:])
    unpad = lambda s: s[:-ord(s[-1:])]
    try:
        enc = base64.b64decode(enc)
    except Exception as e:
        print(decrypt_errmsg(e))
        sys.exit(1)
    iv = enc[:AES.block_size]
    cipher = AES.new(hashed_key, AES.MODE_CFB, iv)
    try:
        b = unpad(base64.b64decode(cipher.decrypt(enc[AES.block_size:])).decode('utf8'))
    except Exception as e:
        print(decrypt_errmsg(e))
        sys.exit(1)
    return b


def decrypt_errmsg(e):
    msg = ("The encryption passphrase appears to be incorrect...\n"
           "Unable to decrypt backup contents...\n\nThe exception was: {0}".format(str(e)))
    return(msg)
