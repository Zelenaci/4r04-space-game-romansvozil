import time, socket, threading
from . import config


class Server():

    def __init__(self, server_name):
        self.server_name = server_name
        self.my_ip = [l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] \
        if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) \
        for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0]

        self.find_client_bool = True
        self.server_status = False
        self.connected_client = [None]

        self.data_to_send = []
        self.data_received = []

        self.find_client_thread = threading.Thread(target=self.broadcast_find_client).start()
        self.server_thread = None

    def broadcast_find_client(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        print('Socket for broadcast was created.. ')
        while self.find_client_bool:
            sock.sendto(('spacegame {}'.format(self.server_name)).encode(), (config.BROADCAST_IP, config.PORT))
            time.sleep(1)
        sock.close()
        print('Broadcast socket has been closed.. ')

    def receive_from_client(self):
        while self.server_status:
            data, addr = self.server_socket.recvfrom(config.BUFFER_SIZE)
            if not(addr == self.connected_client[0]):
                self.connected_client = [addr, data]
                print('Client {} has connected.. '.format(addr))
                self.find_client_bool = False
            self.data_received.append(data)
            print(data)

    def server_start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.my_ip, confg.PORT))
        print('Server socket has been created.. ')
        self.server_status = True
        self.receive_from_client_thread = threading.Thread(target=self.receive_from_client).start()
        while self.connected_client == [None]:
            pass
        while self.server_status:
            if self.data_to_send:
                self.server_socket.sendto(self.data_to_send[0].encode(), self.connected_client[0])
                #print('Message "{}" has been sent.. '.format(self.data_to_send[0]))
                self.data_to_send.remove(self.data_to_send[0])
                time.sleep(1/2000)
            else:
                pass
        print('Server has been closed.. ')


if __name__ == '__main__':
    server = Server('server')
    server.server_thread = threading.Thread(target=self.server_start).start()

    #data = ['ahoj', 'jak', 'se', 'mas romco']
    #for i in range(0, len(data)):
    #    server.data_to_send.append(data[i])
    for i in range(0, 5):
        for _ in range(0, 1000):
            server.data_to_send.append('roman je fakt velkej mega borec u know bitch')
        server.data_to_send.append('END')
