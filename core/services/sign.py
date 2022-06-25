from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15


class SignFile:
    def sign_file(self, private_key, filename):
        user_cert = RSA.import_key(private_key.replace('\\n', '\n'))
        h = SHA256.new()

        with open(filename, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                h.update(chunk)

        signature = pkcs1_15.new(user_cert).sign(h).hex()
        pubkey = user_cert.publickey().export_key().decode('utf8')

        return pubkey, signature
