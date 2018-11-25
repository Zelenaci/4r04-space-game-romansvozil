#!/usr/bin/python

import time, socket, threading

BROADCAST_IP = '<broadcast>'
PORT = 60088 #int(input('Write port number please..: '))
BUFFER_SIZE = 1024


class Client():

	def __init__(self, client_name):
		self.client_name = client_name
		self.my_ip = [l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] \
			if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) \
			for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0]

		self.find_server_bool = True
		self.client_status = False
		self.found_servers = {}

		self.data_to_send = [self.client_name]
		self.data_received = []

		self.find_server_thread = threading.Thread(target=self.broadcast_find_server).start()
		time.sleep(1.5)
		self.find_server_bool = False

	def broadcast_find_server(self):
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		sock.bind((BROADCAST_IP, PORT))
		while self.find_server_bool:
			data, addr = sock.recvfrom(BUFFER_SIZE)
			data = (data.decode()).split()
			if data[0] == 'spacegame' and not(data[1] in self.found_servers):
				self.found_servers[data[1]] = addr[0]
		sock.close()
		print('Broadcast socket has been closed.. ')

	def receive_from_server(self):
		while self.client_status:
			data, addr = self.client_socket.recvfrom(BUFFER_SIZE)
			#data = data.decode()
			self.data_received.append(data)
			if data == b'END':
				print(len(self.data_received))
				self.data_received = []

	def client_start(self, addr):
		self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		print('Client socket has been created.. ')
		self.client_status = True
		self.receive_thread = threading.Thread(target=self.receive_from_server).start()

		while self.client_status:
			if self.data_to_send:
				self.client_socket.sendto(self.data_to_send[0].encode(), (addr, PORT))
				print('Message "{}" has been sent.. '.format(self.data_to_send[0]))
				self.data_to_send.remove(self.data_to_send[0])
				time.sleep(1/2000)


if __name__ == '__main__':
	client = Client('client')
	data = ['snad', 'to', 'funguje jinak se zabiju']
	for i in range(0, len(data)):
		client.data_to_send.append(data[i])
	server_choice = input('{0} '.format(client.found_servers))
	client.client_thread = threading.Thread(target=client.client_start(client.found_servers[server_choice])).start()
#time.sleep(2)
#client.find_server_bool = False
#server_choice = input('{0} '.format(client.found_servers))
#client.client_start(client.found_servers[server_choice])
