import io
import cv2
import random
import socket, select
from time import gmtime, strftime
from random import randint

HOST = '127.0.0.1'
PORT = 9090


for i in range(1, 6):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (HOST, PORT)
    sock.connect(server_address)
    try:
        # open image
        img = cv2.imread(f'images/2/{i}.jpg')
        is_success, im_buf_arr = cv2.imencode(".jpg", img)
        byte_im = im_buf_arr.tobytes()

        size = len(byte_im)
        
        # send image size to server
        sock.sendall(str.encode(f"SIZE {size}"))
        answer = sock.recv(4096)

        print(f'Answer : {answer.decode()}')

        # # send image to server
        if answer.decode().split(':')[0] == 'Got Size ':
            sock.sendall(byte_im)

            # check what server send
            answer = sock.recv(4096)
            print(f'Answer : {answer.decode()}')

            if answer.decode() == 'Got Image' :
                sock.sendall(str.encode("BYE BYE "))
                print('Image successfully send to server')

        sock.close()

    finally:
        sock.close()