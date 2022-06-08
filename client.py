import socket, time, os

# Constants
HOST = "localhost"
PORT = 5000
BUFFER_SIZE = 1024

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

if client_socket.connect:
    data = client_socket.recv(1024)
    data = data.decode()
    while True:
        command = input("Input your command > ")
        cmd = command.split()[0]

        if cmd == "USER":
            username = input("Input username: ")
            cmduser = 'USER {}'.format(username)
            client_socket.send(cmduser.encode())
            user_msg = client_socket.recv(4096)
            print(user_msg.decode())
            
            password = input("Input password: ")
            cmdpass = 'PASS {}'.format(password).encode()
            client_socket.send(cmdpass)
            user_msg = client_socket.recv(1024)
            print(user_msg.decode())
        
        elif cmd == "QUIT":
            client_socket.send(cmd)
            user_msg = client_socket.recv(10000)
            print(user_msg.decode())
            break

        elif cmd == "STOR":
            fn = input("Input file name to be uploaded: ")
            command = ("STOR {}".format(fn).encode())
            client_socket.send(command)

            file_name = command.split()[1]
            local = os.getcwd()
            path = os.path.join(local, 'download')
            upload = os.path.join(path, file_name)
            check = os.path.isfile(upload)
            file_size = os.path.getsize(upload)

            client_socket.send(str(check))
            client_socket.send(str(file_size))
            data = ""

            if check:
                user_msg = client_socket.recv(4096)
                print(user_msg.decode())
 
                with open(upload, 'rb') as f:
                    while file_size:
                        data += f.read()
                        file_size -= len(data)
                client_socket.sendall(data)

            user_msg = client_socket.recv(4096)
            print(user_msg.decode())

        elif cmd == 'RETR':
            fn = input("Input file name to be downloaded: ")
            command = ("RETR {}".format(fn).encode())
            client_socket.send(command)

            file_name = command.split()[1]
            local = os.getcwd()
            path = os.path.join(local, 'download')
            download = os.path.join(path, file_name)
            check = client_socket.recv(4)
            file_size = int(client_socket.recv(4096))
            data=""
            
            if check == 'True':
                user_msg = client_socket.recv(4096)
                print(user_msg.strip().decode())
                
                # print(client_socket.getpeername().decode())
                with open(download, 'wb') as f:
                    while file_size:
                        data = client_socket.recv(4096)
                        f.write(data)
                        file_size -= len(data)
                        
            user_msg = client_socket.recv(4096)
            print(user_msg.strip().decode())

        elif cmd == 'RNFR':
            fn = input("Input file or directory name to be renamed: ")
            command = ("RNFR {}".format(fn).encode())

            client_socket.send(command)
            user_msg = client_socket.recv(10000)
            print(user_msg.decode())

            if '350' in user_msg:
                new = input("Input new directory name: ")
                command = ("RNTO {}".format(fn).encode())
                client_socket.send(command.encode())
            
            user_msg = client_socket.recv(10000)
            print(user_msg.decode())
                        
        else:
            user_msg = client_socket.recv(10000)
            print(user_msg.strip().decode())

client_socket.close()
