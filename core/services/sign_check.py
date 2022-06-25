from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15


class SignFileCheck:
    def verify(self, filename, public_key, signature):
        user_cert = RSA.import_key(public_key.replace('\\n', '\n'))
        h = SHA256.new()
        with open(filename, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                h.update(chunk)

        try:
            pkcs1_15.new(user_cert.publickey()).verify(h, bytes.fromhex(signature))
            return True
        except ValueError as e:
            return False
