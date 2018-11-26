import time, socket, threading
from . import config


class Client():

	def __init__(self, client_name):
		self.client_name = client_name
		self.my_ip = [l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] \
			if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) \
			for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0]

		self.found_servers = {}
		self.connected_to = None

		self.data_to_send = [self.client_name]
		self.data_received = []

		self.find_server_thread = None
		self.client_thread = None

	def broadcast_find_server(self):
		self.broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.broadcast_socket.bind((config.BROADCAST_IP, config.PORT))
		try:
			while True:
				data, addr = self.broadcast_socket.recvfrom(config.BUFFER_SIZE)
				data = (data.decode()).split()
				if data[0] == 'spacegame' and not(data[1] in self.found_servers):
					self.found_servers[data[1]] = addr[0]
		except:
			print('Broadcast socket has been closed.. ')

	def receive_from_server(self):
		try:
			while True:
				data, addr = self.client_socket.recvfrom(config.BUFFER_SIZE)
				self.data_received.append(data)
		except:
			print('Client(receive) has been closed.. ')

	def client_start(self, addr):
		self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.receive_thread = threading.Thread(target=self.receive_from_server).start()
		print('Client socket has been created.. ')

		try:
			while True:
				if self.data_to_send:
					self.client_socket.sendto(self.data_to_send[0].encode(), (addr, config.PORT))
					self.data_to_send.remove(self.data_to_send[0])
					time.sleep(1/2000)
		except:
			print('Client has been closed.. ')
