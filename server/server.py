import socket, threading, select, sys, os
from menus import fquit, fcwd, retr, stor, rnfr, dele, flist, fhelp, rmd, mkd, pwd

# Constants
HOST = "localhost"
PORT = 5000
BUFFER_SIZE = 1024
DATASET = './dataset'
CURRDIR = os.path.abspath('.')

username = 'inez'
password = 'progjarc'

class ThreadedServer:
    def __init__(self):
        self.host = HOST
        self.port = PORT
        self.size = BUFFER_SIZE
        self.server_socket = None
        self.threads = []

    # Initialization
    def open_socket(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print('--- Server is running ---')

    def run(self):
        self.open_socket()
        input_socket = [self.server_socket]

        while True:
            # select socket
            read_ready, write_ready, exception = select.select(input_socket, [], [])
            for sock in read_ready:
                if sock == self.server_socket:
                    # handle server socket
                    # enable to handle multiclient by multithreading
                    client_socket = FTPthread(self.server_socket.accept())
                    client_socket.start()
                    self.threads.append(client_socket)
                elif socket == sys.stdin:
                    # handle standard input
                    junk = sys.stdin.readline()
                    break
        self.server_socket.close()
        for client_socket in self.threads:
            client_socket.join()
        
                    
class FTPthread(threading.Thread):
    def __init__(self, xxx_todo_changeme):
        (conn, addr) = xxx_todo_changeme
        self.conn = conn
        self.addr = addr
        self.size = BUFFER_SIZE * 4
        self.workdir = CURRDIR
        self.cwd = self.workdir
        self.rest = False
        self.pasv_mode = False
        self.passwd = ''
        threading.Thread.__init__(self)

    # Show menu when client connected succesfully
    def run(self):
        self.welcome_message()
        self.user_authentication()

    def welcome_message(self):
        self.welcome_msg = "220 Service ready for new user.\r\n"
        print ('Respon: ' + self.welcome_msg.strip())
        print(self.conn.getpeername())
        print("\n")
        self.conn.send(self.welcome_msg.encode())

    def user_authentication(self):
        self.cmd = (self.conn.recv(self.size)).decode()
        print(("Command: " + self.cmd.strip()))
        print(self.conn.getpeername())
        print("\n")
        command = (self.cmd.split()[0])
        print(command)

        if command == 'USER':
            for line in open('account.txt', 'r').readlines():
                # Split on the space, and store the results in a list of two strings
                auth_info = line.split()
                input_name = (self.cmd.split()[1])

                if input_name == auth_info[0]:
                    self.login_message = '331 User name okay, need password.\r\n'
                    print('Response: ' + self.login_message.strip())
                    print(self.conn.getpeername())
                    print("\n")
                    self.conn.send(self.login_message.encode())

                    self.cmd = (self.conn.recv(self.size)).decode()
                    command = self.cmd.split()[0]
                    
                    if command == "PASS":
                        input_password = self.cmd.split()[1]
                        if input_password == auth_info[1]:
                            self.login_message = '230 User logged in, proceed.\r\n'
                            self.conn.send(self.login_message.encode())
                            print("Response: " + self.login_message.strip())
                            print(self.conn.getpeername())
                            print("\n")
                            self.login_menu()
                        else:
                            self.login_message = "530 Incorrect username or password\r\n"
                            self.conn.send(self.login_message.encode())
                            print("Response: " + self.login_message.strip())
                            print(self.conn.getpeername())
                            print("\n")
                            self.user_authentication()
        else:
            self.message = "500 Syntax error, command unrecognized.\r\n"
            self.login_message = "530 Login required\r\n"
            print("Response: " + self.message.strip())
            print(self.conn.getpeername())
            print("\n")
            print("Response: " + self.login_message.strip())
            print(self.conn.getpeername())
            print("\n")
            self.conn.sendall((self.message + self.login_message).encode())
            self.user_authentication
    
    
        
    def login_menu(self):
        cmd = (self.conn.recv(self.size)).decode()
        print("Command: " + self.cmd.strip())
        print(self.conn.getpeername())
        print("\n")
        command = cmd.split()[0]

        if command == "QUIT":
            fquit(self)
        elif command == "CWD":
            fcwd(self, cmd)
        elif command == "RETR":
            retr(self, cmd)
        elif command == "RNFR":
            rnfr(self, cmd)
        elif command == "DELE":
            dele(self, cmd)
        elif command == "RMD":
            rmd(self, cmd)
        elif command == "MKD":
            mkd(self, cmd)
        elif command == "PWD":
            pwd(self, cmd)
        elif command == "LIST":
            flist(self, cmd)
        elif command == "STOR":
            stor(self, cmd)
        elif command == "HELP":
            fhelp(self, cmd)
        else:
            self.message = "500 Syntax error, command unrecognized.\r\n"
            print("Respon: " + self.message.strip())
            print(self.conn.getpeername())
            print("\n")
            self.conn.send(self.message.encode())
            self.login_menu()
        
    


if __name__ == '__main__':
    s = ThreadedServer()
    s.run()