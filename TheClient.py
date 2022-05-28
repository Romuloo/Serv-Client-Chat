import errno
import select
import socket
import sys


class Client:

    def __init__(self, ip='127.0.0.1', port=1234):
        self.username_h = None
        self.username = None
        self.user = None

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connectSocket(ip, port)
        self.lista = [self.s, sys.stdin]
        self.s.setblocking(False)
        self.register()
        print('----------------------')
        print('Bienvenido al chat de Comandantes de la República ' + str(self.user))
        print('----------------------')
        self.actionPerform()

    def connectSocket(self, ip, port):
        self.s.connect((ip, port))

    def getSocket(self):
        return self.s

    def register(self):
        print("----------- What'Star -----------")
        self.user = input("Indentifíquese: ")
        self.username = self.user.encode('utf-8')
        self.username_h = f"{len(self.username):<{10}}".encode('utf-8')
        self.s.send(self.username_h + self.username)

    def actionPerform(self):
        while True:
            ready, _, _ = select.select(self.lista, [], [])
            for sok in ready:
                if sok == sys.stdin: #Enviar
                    msg = input()
                    if msg == "/close":
                        sys.exit()
                    if len(msg) > 0:
                        msg = msg.encode('utf-8')
                        message_h = f"{len(msg):<{10}}".encode('utf-8')
                        self.s.send(message_h + msg)
                else: #Recibir
                    use_h = self.s.recv(10)
                    if not len(use_h):
                        print('Conexión terminada')
                        sys.exit()
                    user_len = int(use_h.decode('utf-8').strip())
                    username = self.s.recv(user_len).decode('utf-8')
                    message_h = self.s.recv(10)
                    message_len = int(message_h.decode('utf-8').strip())
                    message = self.s.recv(message_len).decode('utf-8')

                    print(f'{username} > {message}')
            if not ready:
                print("--- OUT ---")


c = Client()