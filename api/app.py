from flask import Flask,jsonify,request
from PIL import Image 
import numpy as np
import pyrebase
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

app=Flask(__name__)

firebaseConfig = {
  "apiKey": "AIzaSyBycwJKZ1iKNQeVBZdl40cosXZ8FQNkAg8",
  "authDomain": "cipher-media-e414c.firebaseapp.com",
  "projectId": "cipher-media-e414c",
  "storageBucket": "cipher-media-e414c.appspot.com",
  "messagingSenderId": "737707024550",
  "appId": "1:737707024550:web:ab37d3e1c03dec51005467",
  "databaseURL":""
}

def msg_to_bin(msg):  
    if type(msg) == str:  
        return ''.join([format(ord(i), "08b") for i in msg])  
    elif type(msg) == bytes or type(msg) == np.ndarray:  
        return [format(i, "08b") for i in msg]  
    elif type(msg) == int or type(msg) == np.uint8:  
        return format(msg, "08b")  
    else:  
        raise TypeError("Input type not supported")  

def Encode(src, message, dest):

    img = Image.open(src, 'r')
    width, height = img.size
    array = np.array(list(img.getdata()))

    if img.mode == 'RGB':
        n = 3
    elif img.mode == 'RGBA':
        n = 4

    total_pixels = array.size//n
    
    b_message = msg_to_bin(message)
    req_pixels = len(b_message)

    if req_pixels > (total_pixels * 3):
        print("ERROR: Need larger file size")

    else:
        index=0
        for p in range(total_pixels):
            for q in range(0, 3):
                if index < req_pixels:
                    array[p][q] = int(bin(array[p][q])[2:][-1] + b_message[index], 2)
                    index += 1

        array=array.reshape(height, width, n)
        enc_img = Image.fromarray(array.astype('uint8'), img.mode)
        enc_img.save(dest)
        print("Image Encoded Successfully")

@app.route("/encrypt",methods=['GET'])
def encrypt():
    text=request.args.get('msg')
    img_name=request.args.get("img")
    firebase_storage=pyrebase.initialize_app(firebaseConfig)
    storage=firebase_storage.storage()
    storage.child(img_name).download("./",img_name)
    key = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(text.encode('utf-8'))
    name=img_name.split('.')[0]
    Encode(f'./{img_name}',ciphertext,f'{name}_enc.png')
    return jsonify({"output":"success"})
@app.route("/decrypt",methods=['GET'])
def decrypt():
    img_name=request.args.get("img")
    key=request.args.get("key")
    firebase_storage=pyrebase.initialize_app(firebaseConfig)
    storage=firebase_storage.storage()
    storage.child(img_name).download("./",img_name)
    decoded_text=decode(img_name)
    nonce=123
    cipher = AES.new(key, AES.MODE_EAX, nonce)
    tag=0

    data = cipher.decrypt_and_verify(decoded_text, tag)
    return jsonify({"output":data})
def decode(src):

    img = Image.open(src, 'r')
    array = np.array(list(img.getdata()))

    if img.mode == 'RGB':
        n = 3
    elif img.mode == 'RGBA':
        n = 4

    total_pixels = array.size//n
    hidden_bits = ""
    for p in range(total_pixels):
        for q in range(0, 3):
            hidden_bits += (bin(array[p][q])[2:][-1])

    hidden_bits = [hidden_bits[i:i+8] for i in range(0, len(hidden_bits), 8)]

    message = ""
    
    for i in range(len(hidden_bits)):
        x = len(password)
        if message[-x:] == password:
            break
        else:
            message += chr(int(hidden_bits[i], 2))
    #verifying the password
    if password in message:
        print("Hidden Message:", message[:-x])
        return message[:-x]
    else:
        print("You entered the wrong password: Please Try Again")

if __name__ == '__main__':
    app.run()