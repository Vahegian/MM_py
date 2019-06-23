# from Crypto.Cipher import AES
from Crypto.Cipher import AES
import time

class Encdec:
    def __init__(self):
        # self.worker = None
        self.key= b'!+@_#)$(%*^&~i6:'
        self.enc_nonce = None

    # def init_worker(self, ):
        # self.worker = AES.new(key, AES.MODE_CTR)

    def setKey(self, key):
        self.key = key.encode('UTF-8')

    def setNonce(self, nonce):
        self.enc_nonce = nonce

    def enc(self, message):
        # enc, tag = self.worker.encrypt_and_digest(message)
        # if len(message) < 16:
        #     message = message.decode('utf-8')+('$'*(16-len(message)))
        # print(message)
        # message = message.encode('utf-8')
        enc = AES.new(self.key, AES.MODE_EAX)
        self.enc_nonce = enc.nonce
        ciphertext, tag = enc.encrypt_and_digest(message)
        return (ciphertext, self.enc_nonce)

    def dec(self, enc_message):
        dec = AES.new(self.key, AES.MODE_EAX, nonce=self.enc_nonce)
        return dec.decrypt(enc_message)


if __name__ == "__main__":
    ed = Encdec()
    # ed.init_worker()
    msg = b'0123'
    ed.setKey('1029384756125673')
    enc, nonce = ed.enc(msg)
    print(enc, " : ", nonce)
    time.sleep(2)
    # ed.init_worker()
    print(type(enc), type(nonce))
    ed.setNonce(nonce)
    dec = ed.dec(enc)
    print(dec.decode('utf-8'))