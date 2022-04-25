import os
import glob
import socket, select
from random import randint
from time import gmtime, strftime
from marger import merge_images_horizontally

HOST = '127.0.0.1'
PORT = 9090

connected_clients_sockets = list()
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen(10)
connected_clients_sockets.append(server_socket)

imgcounter = 0

while True:
	read_sockets, write_sockets, error_sockets = select.select(connected_clients_sockets, [], [])
	for sock in read_sockets:
		if sock == server_socket:
			sockfd, client_address = server_socket.accept()
			connected_clients_sockets.append(sockfd)
		else:
			try:
				data = sock.recv(40960000)
				if data:
					if data.startswith(str.encode('SIZE')):
						txt = data.decode()
						tmp = txt.split()
						size = int(tmp[1])
						print(f'Got Size : {size}')
						sock.sendall(str.encode(f'Got Size : {size}'))
					elif data.startswith(str.encode('BYE')):
						sock.shutdown()
					else:
						myfile = open(f'img_{imgcounter}.jpg', 'wb')
						print(myfile)
						if not data: myfile.close(); break
						myfile.write(data)
						myfile.close()

						sock.sendall(str.encode('Got Image'))
						
						if imgcounter == 5:
							print('Marger Image')
							img_list = glob.glob('./img_*.jpg')
							print(img_list)
							file_saved = merge_images_horizontally(img_list)
							print(f'Saved Marger Image : {file_saved}')
							[os.remove(i) for i in img_list]
							imgcounter = 0
						sock.shutdown()
					imgcounter += 1
						
			except:
				sock.close()
				connected_clients_sockets.remove(sock)
				continue
server_socket.close()
		 
