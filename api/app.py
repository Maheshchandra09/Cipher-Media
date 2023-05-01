from flask import Flask,jsonify,request
from PIL import Image 
import numpy as np
import pyrebase
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
password="hi"
def Encode(src, message, dest):

    img = Image.open(src, 'r')
    width, height = img.size
    array = np.array(list(img.getdata()))

    if img.mode == 'RGB':
        n = 3
    elif img.mode == 'RGBA':
        n = 4

    total_pixels = array.size//n

    message+=password 
    b_message = ''.join([format(ord(i), "08b") for i in message])
    req_pixels = len(b_message)

    if req_pixels > (total_pixels * 3):
        print("ERROR: Need larger file size")

    else:
        index=0
        for p in range(total_pixels):
            for q in range(0, 3):
                if index < req_pixels:
                    array[p][q] = int(bin(array[p][q])[2:9] + b_message[index], 2)
                    index += 1

        array=array.reshape(height, width, n)
        enc_img = Image.fromarray(array.astype('uint8'), img.mode)
        enc_img.save(dest+"/output.jpg")
        print("Image Encoded Successfully")

@app.route("/Encode",methods=['GET'])
def encrypt():
    # req=request.args.to_dict()
    text=request.args.get('msg')
    # pswd=request.args.get("pwd")
    img_name=request.args.get("img")
    # cipher=DES.new(key,DES.MODE_EAX)
    # nonce=cipher.nonce
    # ciphertext,tag=cipher.encrypt_and_digest(text.encode('ascii'))
    # Encode('../ims.png',ciphertext,'../imse.png',pswd)
    # return send_file('../imse.png',mimetype="image/gif")+"<p> {}</p>".format(nonce)+"<p> {}</p>".format(tag)s
    firebase_storage=pyrebase.initialize_app(firebaseConfig)
    storage=firebase_storage.storage()
    storage.child(img_name).download("./",img_name)
    Encode(f'./{img_name}',text,'./outputs')
@app.route("/Decode",methods=['GET'])
def decode():
    img_name=request.args.get("img")
    firebase_storage=pyrebase.initialize_app(firebaseConfig)
    storage=firebase_storage.storage()
    storage.child(img_name).download("./",img_name)
    img = Image.open("./outputs/output.jpg", 'r')
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
    hiddenmessage = ""
    for i in range(len(hidden_bits)):
        x = len(password)
        if message[-x:] == password:
            break
        else:
            message += chr(int(hidden_bits[i], 2))
            message = f'{message}'
            hiddenmessage = message
    #verifying the password
    if password in message:
        print("Hidden Message:", hiddenmessage[:-x])
    else:
        print("You entered the wrong password: Please Try Again")
    d={}
    d['output']=hiddenmessage[:-x]
    return jsonify(d)
    # cipher=DES.new(key,DES.MODE_EAX,nonce=nonce)
    # plaintext=cipher.decrypt(hiddenmessage[:-x])

    # try:
    #     cipher.verify(tag)
    #     return "<p>  Text decoded is {} </p>".format(plaintext.decode('ascii'))
    # except:
    #     return False

if __name__ == '__main__':
    app.run()