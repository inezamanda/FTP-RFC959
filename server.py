import socket, threading, select, sys, os

# Constants
HOST = "localhost"
PORT = 5000
BUFFER_SIZE = 1024
DATASET = './dataset'
CURRDIR = os.path.abspath('.')

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
    def __init__(self, conn, addr):
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
        self.welcome_message = "220 Service ready for new user.\r\n"
        print ('Respon: ' + self.welcome_message.strip())
        print(self.conn.getpeername())
        self.conn.send(self.welcome_message)

    def user_authentication(self):
        self.cmd = self.conn.recv(self.size)
        print("Command: " + self.cmd.strip())
        print(self.conn.getpeername())
        command = self.cmd.split()[0]

        if command == 'USER':
            for line in open('account.txt', 'r').readlines():
                # Split on the space, and store the results in a list of two strings
                auth_info = line.split()

                input_name = self.cmd.split()[1]
                if input_name == auth_info[0]:
                    self.login_message = '331 User name okay, need password.\r\n'
                    print('Response: ' + self.login_message.strip(), self.conn.getpeername())
                    self.conn.send(self.login_message)

                    self.cmd = self.conn.recv(self.size)
                    command = self.cmd.split()[0]
                    
                    if command == "PASS":
                        input_password = self.cmd.split()[1]

                        if input_password == auth_info[1]:
                            self.login_message = '230 User logged in, proceed.\r\n'
                            self.conn.send(self.login_message)
                            print("Response: " + self.login_message.strip())
                            print(self.conn.getpeername())
                            self.login_menu()
                        else:
                            self.login_message = "530 Incorrect username or password\r\n"
                            self.conn.send(self.login_message)
                            print("Response: " + self.login_message.strip())
                            print(self.conn.getpeername())
                            self.user_authentication()
        else:
            self.message = "500 Syntax error, command unrecognized.\r\n"
            self.login_message = "530 Login required\r\n"
            print("Response: " + self.message.strip())
            print(self.conn.getpeername())
            print("Response: " + self.login_message.strip())
            print(self.conn.getpeername())
            self.conn.sendall(self.message + self.login_message)
            self.user_authentication
    
    def login_menu(self):
        cmd = self.conn.recv(self.size)
        print("Command: " + self.message.strip())
        print(self.conn.getpeername())
        command = cmd.split()[0]

        if command == "QUIT":
            fquit(cmd)
        elif command == "CWD":
            fcwd(cmd)
        elif command == "RETR":
            retr(cmd)
        elif command == "RNFR":
            rnfr(cmd)
        elif command == "DELE":
            dele(cmd)
        elif command == "RMD":
            rmd(cmd)
        elif command == "MKD":
            mkd(cmd)
        elif command == "PWD":
            pwd(cmd)
        elif command == "LIST":
            flist(cmd)
        elif command == "HELP":
            fhelp(cmd)
        else:
            self.message = "500 Syntax error, command unrecognized.\r\n"
            print("Respon: " + self.message.strip())
            print(self.conn.getpeername())
            self.conn.send(self.message)
            self.login_menu()
        
    def fquit(self, cmd):
        self.login_message = "221 Service closing control connection.\r\n"
        self.conn.send(self.login_message)
        print("Respon: " + self.login_message.strip())
        print(self.conn.getpeername())
        self.conn.close()
    
    def fcwd(self, cmd):
        chwd = cmd.split()[1]
        if chwd == '/':
            self.cwd = self.workdir
        elif chwd[0] == '/':
            self.cwd = os.path.join(self.workdir, cmd.split()[1])
        else:
            self.cwd = os.path.join(self.cwd, chwd)
        self.conn.send('250 Requested file action okay, completed.\r\n')
        self.login_menu()
    
    def retr(self, cmd):
        file_name = cmd.split()[1]
        path = os.path.join(self.cwd, file_name)
        check = os.path.isfile(path)
        file_size = os.path.getsize(path)
        print('Download: ', file_name)
        self.conn.send('File exist: ' + str(check))
        self.conn.send('File size: ' + str(file_size))
        data = ""

        if check:
            with open(path, 'rb') as f:
                while file_size:
                    data += f.read()
                    file_size -= len(data)
            self.conn.sendall(data)
            self.message = '226 Closing data connection. Requested file action successful\r\n'
            print("Response: " + self.message.strip())
            print(self.conn.getpeername())
            self.conn.send(self.message)
        else:
            self.message = "501 Syntax error in parameters or arguments.\r\n"
            print("Response: " + self.message.strip())
            print(self.conn.getpeername())
            self.conn.send(self.message)
        
        self.login_menu()
    
    def rnfr(self, cmd):
        file_name = cmd.split()[1]
        path = os.path.join(self.cwd, file_name)
        checkDir = os.path.isdir(path)
        checkFile = os.path.isfile(path)

        if checkDir:
            self.message = "350 Requested file action pending further information.\r\n"
            print("Response: " + self.message.strip())
            print(self.conn.getpeername())
            self.conn.send(self.message)
            cmd = self.conn.recv(self.size)
            if 'RNTO' in cmd:
                print("Command: " + cmd.strip())
                print(self.conn.getpeername())
                name = os.path.join(self.cwd, self.command.strip().split(' ')[1]) 
                rename = os.rename(path, name)
                self.message = '250 Requested file action okay, completed.\r\n'
                print('Response: ' + self.message.strip())
                print(self.conn.getpeername())
                self.conn.send(self.message)
            else:
                self.message = '501 Syntax error in parameters or arguments.\r\n'
                print('Response: ' + self.message.strip())
                print(self.conn.getpeername())
                self.conn.send(self.message)
            self.login_menu()

    def dele(self, cmd):
        self.chwd = cmd.split()[1]
        file_name = os.path.join(self.cwd, self.chwd)
        self.allow_delete = os.path.isfile(file_name)
        if self.allow_delete:
            os.remove(file_name)
            self.message = '250 Requested file action okay, completed.\r\n'
            print('Response: ' + self.message.strip())
            print(self.conn.getpeername())
            self.conn.send(self.message)
        else:
            self.conn.send('450 Requested file action not taken.\nFile unavailable (e.g., file busy).\r\n')  
        self.login_menu()

    def rmd(self, cmd):
        self.chwd = cmd.split()[1]
        dir_name = os.path.join(self.cwd, self.chwd)
        self.allow_delete = os.path.isdir(dir_name)

        if self.allow_delete:
            os.rmdir(dir_name)
            self.message = '250 Requested file action okay, completed.\r\n'
            print('Response: ' + self.message.strip())
            print(self.conn.getpeername())
            self.conn.send(self.message)
        else:
            self.message = '550 Requested action not taken.\nFile unavailable (e.g., file not found, no access).\r\n'
            print('Response: ' + self.message.strip())
            print(self.conn.getpeername())
            self.conn.send(self.message)
        self.login_menu()

    def mkd(self, cmd):
        self.chwd = cmd.split()[1]
        dir_name = os.path.join(self.cwd, self.chwd)
        self.allow_make = os.path.isdir(dir_name)
        if self.allow_make:
            self.message = '550 Requested action not taken.\nFile unavailable (e.g., file not found, no access).\r\n'
            print('Response: ' + self.message.strip())
            print(self.conn.getpeername())
            self.conn.send(self.message)
        else:
            os.mkdir(dn)
            self.message = '250 Requested file action okay, completed.\r\n'
            print('Response: ' + self.message.strip())
            print(self.conn.getpeername())
            self.conn.send(self.message)  
        self.login_menu()

    def pwd(self, cmd):
        cwd = os.path.relpath(self.cwd, self.workdir)
        if cwd == '.':
            cwd = '/'
        else:
            cwd = '/'+cwd
        self.message = '257 ' + self.cwd + ' is current directory.\r\n'
        print('Response: ' + self.message.strip())
        print(self.conn.getpeername())
        self.conn.send(self.message)
        self.login_menu()
    
    def flist(self, cmd):
        message = ('150 File status okay; about to open data connection.\n')
        dirList = os.listdir(self.cwd)
        for x in dirList:
            temp = os.path.join(self.cwd, x)
            message = message + temp + '\n'
        self.conn.send(message)
        self.conn.send('226 Closing data connection.\nRequested file action successful (for example, file transfer or file abort).')
        self.login_menu()

    def fhelp(self, cmd):
        self.conn.send(
            '214 The following commands are recognized:\nUSER PASS CWD QUIT RETR STOR RNFR RNTO DELE RMD MKD PWD LIST HELP\r\n')
        self.login_menu()


if __name__ == '__main__':
    s = ThreadedServer()
    s.run()