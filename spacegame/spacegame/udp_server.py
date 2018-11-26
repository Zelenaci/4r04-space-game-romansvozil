import time, socket, threading
from . import config


class Server():

    def __init__(self, server_name):
        self.server_name = server_name
        self.my_ip = [l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] \
        if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) \
        for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0]

        self.connected_client = []

        self.data_to_send = []
        self.data_received = []

        self.find_client_thread = None
        self.server_thread = None

    def broadcast_find_client(self):
        self.broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        print('Socket for broadcast was created.. ')
        try:
            while True:
                self.broadcast_socket.sendto(('spacegame {0}'.format(self.server_name)).encode(), (config.BROADCAST_IP, config.PORT))
                time.sleep(1)
        except:
            print('Broadcast socket has been closed.. ')

    def receive_from_client(self):
        try:
            while True:
                data, addr = self.server_socket.recvfrom(config.BUFFER_SIZE)
                if self.connected_client == []:
                    self.connected_client = [addr, data.decode()]
                    print('Client {} has connected.. '.format(addr))
                self.data_received.append(data)
        except:
            print('Server(receive) has been closed.. ')

    def server_start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.my_ip, config.PORT))
        print('Server socket has been created.. ')
        self.receive_from_client_thread = threading.Thread(target=self.receive_from_client).start()
        while self.connected_client == []:
            pass
        try:
            while True:
                if self.data_to_send:
                    self.server_socket.sendto(self.data_to_send[0].encode(), self.connected_client[0])
                    self.data_to_send.remove(self.data_to_send[0])
                    time.sleep(1 / config.FPS)
                else:
                    pass
        except:
            print('Server has been closed.. ')
