import select
import socket


class Server:

    def __init__(self, ip='127.0.0.1', port=1234, n=5):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.bindSocket(ip, port)
        self.listenSocket(n)
        print('-------- Servidor activo --------')
        self.clients = {}
        self.sockets = [self.s]
        self.manageClients()

    def getSocket(self):
        return self.s

    def bindSocket(self, ip, port):
        self.s.bind((ip, port))

    def listenSocket(self, n):
        self.s.listen(n)

    def receive_msg(self, sck):
        encabezado = sck.recv(10)
        if not len(encabezado):
            return False
        leng = int(encabezado.decode('utf-8').strip())
        return {'header': encabezado, 'data': sck.recv(leng)}

    def register_users(self, sct):
        newSocket, ip = sct.accept()
        user = self.receive_msg(newSocket)
        self.sockets.append(newSocket)
        self.clients[newSocket] = user
        print("Usuario registrado")

    def close_conection(self, sct):
        print('Conexion terminada.')
        del self.clients[sct]
        self.sockets.remove(sct)

    def manageClients(self):
        global newMsg
        while True:
            r, _, _ = select.select(self.sockets, [], [])
            for sct in r:
                if sct == self.s:
                    self.register_users(sct)
                else:
                    msg = self.receive_msg(sct)
                    if not msg:
                        self.close_conection(sct)
                        continue
                    if msg['data'].decode('utf-8')[0:5] == '/priv':
                        dest_priv = {}
                        for s in self.clients:
                            try:
                                if self.clients[s]['data'].decode('utf-8') == msg['data'].decode('utf-8').split()[1]:
                                    lenDestinatario = len(msg['data'].decode('utf-8').split()[1])
                                    newMsg = msg
                                    newMsg['data'] = msg['data'][6 + lenDestinatario:]  # así elimino el comando
                                    dest_priv[s] = newMsg
                            except IndexError:
                                continue
                        emisor = self.clients[sct]
                        print(f'{emisor}: {newMsg}')
                        self.send_msgs(sct, emisor, newMsg, dest_priv)

                    else:
                        emisor = self.clients[sct]
                        print(f'{emisor}: {msg}')
                        self.send_msgs(sct, emisor, msg, self.clients)

    def send_msgs(self, sct, emisor, msg, destinatarios):
        for sockt in destinatarios:
            if sockt != sct:
                sockt.send(emisor['header'] + emisor['data'] + msg['header'] + msg['data'])


s = Server()
