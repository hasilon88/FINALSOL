from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from hashlib import sha256
import json

def hash(string):
    return sha256(string.encode('utf-8')).hexdigest()

def encryptString(string, keyFilePath):
    f = open(keyFilePath)
    data = json.load(f)
    f.close()

    encryptedString = ""

    for i in range(len(string)):
        encryptedString += data.get(string[i])
    
    return encryptedString

def decryptString(string, keyFilePath):
    f = open(keyFilePath)
    data = json.load(f)
    f.close()

    reverse_dict = {value: key for key, value in data.items()}

    decryptedString = ""

    for i in range(len(string)):
        decryptedString += reverse_dict.get(string[i], "")

    return decryptedString

def generateKeyPair():
    private_key = rsa.generate_private_key (
    public_exponent=65537,
    key_size=2048,
    backend=default_backend())

    public_key = private_key.public_key()

    return {"public_key": public_key, "private_key": private_key}

def convertKeyPairToStr(keyPair):
    public_key = keyPair.get("public_key")
    private_key = keyPair.get("private_key")

    private_pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()).decode('utf-8')
    
    public_pem = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo).decode('utf-8')

    return {"str_public_key": public_pem, "str_private_key": private_pem}

def convertStrKeyPairToKey(strKeyPair):
    loaded_private_key = serialization.load_pem_private_key(
    strKeyPair.get("str_private_key").encode('utf-8'),
    password=None,
    backend=default_backend())

    loaded_public_key = serialization.load_pem_public_key(
    strKeyPair.get("str_public_key").encode('utf-8'),
    backend=default_backend())

    return {"public_key": loaded_public_key, "private_key":loaded_private_key}

def convertStrPublicKeyToKey(strKey):
    loaded_public_key = serialization.load_pem_public_key(
    strKey.encode('utf-8'),
    backend=default_backend())

    return loaded_public_key

def convertStrPrivateKeyToKey(strKey):
    loaded_private_key = serialization.load_pem_private_key(
    strKey.encode('utf-8'),
    password=None,
    backend=default_backend())

    return loaded_private_key

def convertPublicKetToStr(public_key):
    public_pem = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo).decode('utf-8')

    return public_pem


def encryptWithPublicKey(string, public_key):
    string = string.encode('utf-8')

    ciphertext = public_key.encrypt(
    string,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    ))

    return ciphertext

def decryptWithPrivateKey(encryptedString, private_key):
    decrypted_message = private_key.decrypt(
    encryptedString,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    ))

    return decrypted_message.decode('utf-8')