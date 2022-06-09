import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', 6000))

if s.connect:
    data = s.recv(1024)
    data = data.decode()
    print(data)
    print("Connected to Server")

    while(1):
        command = input("\nInput your command: ")
        if "USER" in command:
            username = input("Input username: ")
            cmduser = 'USER {}'.format(username).encode()
            s.send(cmduser)
            msg = s.recv(1024)
            print(msg.decode())

            password = input("Input password: ")
            cmdpass = 'PASS {}'.format(password).encode()
            s.send(cmdpass)
            msg = s.recv(1024)
            print(msg.decode())

        if "LIST" in command:
            s.send(command.encode())
            msg = s.recv(1024)
            print(msg.decode())

        elif "QUIT" in command:
            s.send(command.encode())
            msg = s.recv(1024)
            print(msg.decode())

        elif "MKD" in command:
            foldername = input("Input directory name to be created: ")
            cmd = ('MKD {}'.format(foldername).encode())
            s.send(cmd)
            msg = s.recv(1024)
            print(msg.decode())

        elif "RMD" in command:
            foldername = input("Input directory name to be removed: ")
            cmd = ('RMD {}'.format(foldername).encode())
            s.send(cmd)
            msg = s.recv(1024)
            print(msg.decode())

        elif "RNFR" in command:
            fn = input("Input file or directory name to be renamed: ")
            cmd = ('RNFR {}'.format(fn).encode())
            new = input("Input new directory name: ")
            command = ('RNTO {}'.format(new).encode())
            s.send(cmd)
            msg1 = s.recv(1024)
            s.send(command)
            msg = s.recv(1024)
            print(msg1.decode())
            print(msg.decode())

        elif "DELE" in command:
            fn = input("Input file name to be deleted: ")
            cmd = ('DELE {}'.format(fn).encode())
            s.send(cmd)
            msg = s.recv(1024)
            print(msg.decode())

        elif "PWD" in command:
            cmd = ('PWD'.encode())
            s.send(cmd)
            msg = s.recv(1024)
            print(msg.decode())

        elif "CWD" in command:
            directory = input("Input directory name to be headed: ")
            cmd = ("CWD {}".format(directory).encode())
            s.send(cmd)
            msg = s.recv(1024)
            print(msg.decode())

        elif "HELP" in command:
            cmd = ("HELP".encode())
            s.send(cmd)
            msg = s.recv(1024)
            print(msg.decode())

        elif "RETR" in command:
            fn = input("Input file name to be downloaded: ")
            cmd = ("RETR {}".format(fn).encode())
            s.send(cmd)
            msg = s.recv(1024)
            print(msg.decode())
            fo = open(fn, 'wb')
            size = int(s.recv(16))

            accepted = ''.encode()
            while size > len(accepted):
                data = s.recv(1024)
                if not data:
                    break
                accepted += data
                fo.write(data)

        elif "STOR" in command:
            fn = input("Input file name to be uploaded: ")
            cmd = ("STOR {}".format(fn).encode())
            s.send(cmd)

            print(fn)
            with open('fn', 'rb') as f:
                data = f.read()
                print(f.read())
            s.sendall(('%16d' % len(data)).encode())
            s.sendall(data)
