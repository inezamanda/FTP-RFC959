import os

def fquit(self):
        self.login_message = "221 Service closing control connection.\r\n"
        self.conn.send(self.login_message.encode())
        print("Respon: " + self.login_message.strip())
        print(self.conn.getpeername())
        print("\n")
        self.conn.close()
    
def fcwd(self, cmd):
        chwd = cmd.split()[1]
        if chwd == '/':
            self.cwd = self.workdir
        elif chwd[0] == '/':
            self.cwd = os.path.join(self.workdir, cmd.split()[1])
        else:
            self.cwd = os.path.join(self.cwd, chwd)
        self.conn.send('250 Requested file action okay, completed.\r\n'.encode())
        self.login_menu()
    
def retr(self, cmd):
        file_name = cmd.split()[1]
        path = os.path.join(self.cwd, file_name)
        check = os.path.isfile(path)
        file_size = os.path.getsize(path)
        print('Download: ', file_name)
        self.conn.send(str(check).encode())
        self.conn.send(str(file_size).encode())
        data = ""

        if check:
            with open(path, 'rb') as f:
                while file_size:
                    data += f.read().decode()
                    file_size -= len(data)
            self.conn.sendall(data.encode())
            self.message = '226 Closing data connection. Requested file action successful\r\n'
            print("Response: " + self.message.strip())
            print(self.conn.getpeername())
            self.conn.send(self.message.encode())
        else:
            self.message = "501 Syntax error in parameters or arguments.\r\n"
            print("Response: " + self.message.strip())
            print(self.conn.getpeername())
            self.conn.send(self.message.encode())
        self.login_menu()
    
def rnfr(self, cmd):
        file_name = cmd.split()[1]
        path = os.path.join(self.cwd, file_name)
        checkDir = os.path.isdir(path)
        checkFile = os.path.isfile(path)
        print(path)

        if checkDir:
            self.message = "350 Ready for RNTO directory\r\n"
            print("Response: " + self.message.strip())
            print(self.conn.getpeername())
            self.conn.send(self.message.encode())
            cmd = (self.conn.recv(self.size)).decode()
            if 'RNTO' in cmd:
                print("Command: " + cmd.strip())
                print(self.conn.getpeername())
                name = os.path.join(self.cwd, cmd.strip().split(' ')[1]) 
                print(name)
                os.rename(path, name)
                self.message = '250 Requested file action okay, completed.\r\n'
                print('Response: ' + self.message.strip())
                print(self.conn.getpeername())
                self.conn.send(self.message.encode())
            else:
                self.message = '501 Syntax error in parameters or arguments.\r\n'
                print('Response: ' + self.message.strip())
                print(self.conn.getpeername())
                self.conn.send(self.message.encode())
            self.login_menu()
        elif checkFile:
            self.message = '350 Ready for RNTO file\r\n'
            print("Response: " + self.message.strip())
            print(self.conn.getpeername())
            self.conn.send(self.message.encode())
            cmd = (self.conn.recv(self.size)).decode()
            if 'RNTO' in cmd:
                print("Command: " + self.message.strip())
                print(self.conn.getpeername())
                name = os.path.join(self.cwd, cmd.strip().split(' ')[1])
                os.rename(path, name)
                self.message = '250 Rename was successful.\r\n'
                print("Response: " + self.message.strip())
                print(self.conn.getpeername())
                self.conn.send(self.message.encode())
            else:
                self.message = '501 Syntax error in parameters or arguments. This usually results from an invalid or missing file name.\r\n'
                print("Response: " + self.message.strip())
                print(self.conn.getpeername())
                self.conn.send(self.message.encode())
            self.login_menu()
        else:
            self.message = '501 Unknown command\r\n'
            print("Response: " + self.message.strip())
            print(self.conn.getpeername())
            self.conn.send(self.message.encode())

def dele(self, cmd):
        self.chwd = cmd.split()[1]
        file_name = os.path.join(self.cwd, self.chwd)
        self.allow_delete = os.path.isfile(file_name)
        if self.allow_delete:
            os.remove(file_name)
            self.message = '250 Requested file action okay, completed.\r\n'
            print('Response: ' + self.message.strip())
            print(self.conn.getpeername())
            self.conn.send(self.message.encode())
        else:
            self.conn.send('450 Requested file action not taken.\nFile unavailable (e.g., file busy).\r\n'.encode())  
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
            self.conn.send(self.message.encode())
        else:
            self.message = '550 Requested action not taken.\nFile unavailable (e.g., file not found, no access).\r\n'
            print('Response: ' + self.message.strip())
            print(self.conn.getpeername())
            self.conn.send(self.message.encode())
        self.login_menu()

def mkd(self, cmd):
        self.chwd = cmd.split()[1]
        dir_name = os.path.join(self.cwd, self.chwd)
        self.allow_make = os.path.isdir(dir_name)
        if self.allow_make:
            self.message = '550 Requested action not taken.\nFile unavailable (e.g., file not found, no access).\r\n'
            print('Response: ' + self.message.strip())
            print(self.conn.getpeername())
            self.conn.send(self.message.encode())
        else:
            os.mkdir(dir_name)
            self.message = '250 Requested file action okay, completed.\r\n'
            print('Response: ' + self.message.strip())
            print(self.conn.getpeername())
            self.conn.send(self.message.encode())  
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
        self.conn.send(self.message.encode())
        self.login_menu()
    
def flist(self, cmd):
        message = ('150 File status okay; about to open data connection.\n')
        dirList = os.listdir(self.cwd)
        for x in dirList:
            temp = os.path.join(self.cwd, x)
            message = message + temp + '\n'
        self.conn.send(message.encode())
        self.conn.send('226 Closing data connection.\nRequested file action successful (for example, file transfer or file abort).'.encode())
        self.login_menu()

def stor(self, cmd):
        print("masuk stor")
        file_name = cmd.split()[1]
        path = os.path.join(self.cwd, file_name)
        check = self.conn.recv(4).decode()
        file_size = int(self.conn.recv(self.size).decode())
        data = ""

        if check == 'True':
            self.message = '150 File status okay; about to open data connection.\r\n'
            print("Respon: " + self.message.strip())
            print(self.conn.getpeername())
            self.conn.send(self.message.encode())

            with open(path, 'wb') as file:
                while file_size:
                    data = self.conn.recv(self.size).decode()
                    if not data:
                        break
                    file.write(data.encode())
                    file_size -= len(data)
            self.message = '226 Closing data connection.\nRequested file action successful (for example, file transfer or file abort).'
            print("Response: " + self.message.strip())
            print(self.conn.getpeername())
            self.conn.send(self.message.encode())
        else:
            self.message = '501 Syntax error in parameters or arguments.\r\n'
            print("Response: " + self.message.strip())
            print(self.conn.getpeername())
            self.conn.send(self.message.encode())
        self.login_menu()    

def fhelp(self, cmd):
        self.conn.send(
            '214 The following commands are recognized:\nUSER PASS CWD QUIT RETR STOR RNFR RNTO DELE RMD MKD PWD LIST HELP\r\n'.encode())
        self.login_menu()